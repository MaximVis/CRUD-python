from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import psycopg2


app = Flask(__name__)

def connect_dbase():
    connect = psycopg2.connect(user="postgres", password="123", host="localhost", port="5433", database = "operator_base")
    return connect

@app.route("/")
def index():
    connect = connect_dbase()
    cursor = connect.cursor()
    cursor.execute('''select calls.*, status_calls.*, to_char(calls.date_time_call, 'hh24:mi, dd-mm-yyyy') as call_time_date from calls inner join status_calls on status_calls.status_call_id = calls.call_status_id order by calls.call_status_id asc, calls.date_time_call desc;''')
    calls = cursor.fetchall()
    cursor.execute('''select * from brigades inner join brigades_calls on brigades.brigade_id = brigades_calls.bc_brigade_id''')
    brigades = cursor.fetchall()
    cursor.execute('''select brigades.*, status_brigades.*, doctor.full_name as doctor_name, paramedic.full_name as paramedic_name, driver.full_name as driver_name, to_char(brigades.date_duty, 'DD:MM:YYYY') as f_date_duty from brigades 
    join status_brigades on brigades.brigade_status_id = status_brigades.status_brigade_id
    left join employees_members as doctor on brigades.brigade_doctor_id = doctor.employee_id
    left join employees_members as paramedic on brigades.brigade_paramedic_id = paramedic.employee_id
    left join employees_members as driver on brigades.brigade_driver_id = driver.employee_id
    order by case when status_brigades.status_brigade_id = 2 then 0 else 1 end;''')
    all_brigades = cursor.fetchall()
    cursor.close()
    connect.close()
    return render_template("index.html", calls = calls, brigades = brigades, all_brigades = all_brigades)


@app.route('/create_call/', methods=('GET', 'POST'))
def create_call():
    connect = connect_dbase()
    cursor = connect.cursor()
    cursor.execute('''select brigades.brigade_id, brigades.brigade_location from brigades where brigade_status_id = 2;''')
    brigades = cursor.fetchall()
    cursor.execute('''SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS');''')
    date_time_call = cursor.fetchall()
    date_time_call = date_time_call[0][0]
    date_format = "%Y-%m-%d %H:%M:%S"
    date_time_call = datetime.strptime(date_time_call, date_format)
    cursor.execute('''select dispatchers.full_name from dispatchers''')
    dispatchers = cursor.fetchall()
    names = [name[0] for name in dispatchers]
    cursor.close()
    connect.close()
    if request.method == 'POST':

        selected_dispatcher = request.form.get('dispatcher')
        dispatcher_id = names.index(selected_dispatcher) + 1
        selected_brigades = request.form.getlist('brigade')
        name_called = request.form['name_called']
        patient_name = request.form['patient_name']
        reason = request.form['reason']
        adres = request.form['adres']

        departure_times = request.form.getlist('departure_time')
        arrival_times = request.form.getlist('arrival_time')
        closure_times = request.form.getlist('closure_time')

        connect = connect_dbase()
        cursor = connect.cursor()
        cursor.execute('''SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS');''')
        time_call_accept = cursor.fetchall()
        time_call_accept = time_call_accept[0][0]
        time_call_accept = datetime.strptime(time_call_accept, date_format)

        call_status_id = check_arr(departure_times, arrival_times, closure_times)

        if (call_status_id == 1):
            cursor.execute('INSERT INTO calls (call_dispatcher_id, call_status_id, date_time_call, time_call_accept, full_name_call, full_name_patient, reason, call_adres, time_call_close)''VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)  RETURNING call_id;',
                (dispatcher_id, 1, date_time_call, time_call_accept, name_called, patient_name, reason, adres, None))
        else:
            cursor.execute('INSERT INTO calls (call_dispatcher_id, call_status_id, date_time_call, time_call_accept, full_name_call, full_name_patient, reason, call_adres, time_call_close)''VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)  RETURNING call_id;',
                (dispatcher_id, 2, date_time_call, time_call_accept, name_called, patient_name, reason, adres, time_call_accept))

        called_id = cursor.fetchone()[0]
        connect.commit()

        for i in range(len(selected_brigades)):
            brig_id = selected_brigades[i].split(',', 1)[0].strip()
            departure_times[i] = check_str(departure_times[i])
            arrival_times[i] = check_str(arrival_times[i])
            closure_times[i] = check_str(closure_times[i])
            cursor.execute('INSERT INTO brigades_calls (bc_call_id, bc_brigade_id, bc_exit, bc_come, bc_return)''VALUES (%s, %s, %s, %s, %s);',
                (called_id, brig_id, departure_times[i], arrival_times[i], closure_times[i],))

        connect.commit()
        cursor.close()
        connect.close()

        return redirect(url_for('index'))

    return render_template('create_call.html', brigades=brigades, dispatchers=names)


@app.route('/edit_call/<int:call_id>', methods=('GET', 'POST'))
def edit_call(call_id):

    connect = connect_dbase()
    cursor = connect.cursor()

    cursor.execute('''select dispatchers.full_name from dispatchers''')
    dispatchers = cursor.fetchall()
    dispatchers = [disp[0] for disp in dispatchers]

    cursor.execute('''select full_name_call from calls where call_id = %s;''', (call_id,))
    name_called = cursor.fetchall()
    name_called = [name[0] for name in name_called]
    name_called = name_called[0]

    cursor.execute('select full_name_patient from calls where call_id = %s', (call_id,))
    patient_name = cursor.fetchall()
    patient_name = [name[0] for name in patient_name]
    patient_name = patient_name[0]

    cursor.execute('select reason from calls where call_id = %s', (call_id,))
    reason = cursor.fetchall()
    reason = [res[0] for res in reason]
    reason = reason[0]

    cursor.execute('select call_adres from calls where call_id = %s', (call_id,))
    adres = cursor.fetchall()
    adres = [adr[0] for adr in adres]
    adres = adres[0]

    cursor.execute('SELECT dispatchers.full_name FROM dispatchers  JOIN calls ON calls.call_dispatcher_id = dispatchers.dispatcher_id WHERE call_id = %s ', (call_id,))
    dispatcher = cursor.fetchall()
    dispatcher = [disp[0] for disp in dispatcher]
    dispatcher = dispatcher[0]

    cursor.execute('''select brigades.brigade_id, brigades.brigade_location from brigades where brigade_status_id = 2;''')
    brigades = cursor.fetchall()
    brigades = [f"{id},{brig}" for id, brig in brigades]

    cursor.execute('select brigades.brigade_id, brigades.brigade_location from brigades join brigades_calls on brigades_calls.bc_brigade_id = brigades.brigade_id where bc_call_id = %s;', (call_id,))
    selected_brigades = cursor.fetchall()
    selected_brigades = [f"{id},{brig}" for id, brig in selected_brigades]


    cursor.execute('select bc_exit from brigades_calls where bc_call_id = %s;',(call_id,))
    departure_Times = cursor.fetchall()
    departure_Times = [time[0].strftime('%H:%M') if time[0] is not None else '' for time in departure_Times]

    cursor.execute('select bc_come from brigades_calls where bc_call_id = %s;', (call_id,))
    Arrival_Times = cursor.fetchall()
    Arrival_Times = [time[0].strftime('%H:%M') if time[0] is not None else '' for time in Arrival_Times]

    cursor.execute('select bc_return from brigades_calls where bc_call_id = %s;', (call_id,))
    Closure_Times = cursor.fetchall()
    Closure_Times = [time[0].strftime('%H:%M') if time[0] is not None else '' for time in Closure_Times]

    cursor.close()
    connect.close()
    if request.method == 'POST':

        selected_dispatcher = request.form.get('dispatchers')
        dispatcher_id = dispatchers.index(selected_dispatcher) + 1
        name_called = request.form['name_called']
        patient_name = request.form['patient_name']
        reason = request.form['reason']
        adres = request.form['adres']

        new_selected_brigades = request.form.getlist('brigade')
        departure_times = request.form.getlist('departure_time')
        arrival_times = request.form.getlist('arrival_time')
        closure_times = request.form.getlist('closure_time')

        connect = connect_dbase()
        cursor = connect.cursor()

        cursor.execute('select call_status_id from calls where call_id = %s;', (call_id,))
        call_status_id = cursor.fetchall()
        call_status_id = [cs[0] for cs in call_status_id]
        call_status_id = call_status_id[0]

        if(call_status_id == 1 and departure_times and arrival_times and closure_times):
            call_status_id = check_arr(departure_times, arrival_times, closure_times)
            if (call_status_id == 1):
                cursor.execute('''update calls set call_dispatcher_id = %s, full_name_call = %s, full_name_patient = %s, reason = %s, call_adres  = %s where call_id = %s;''',
                (dispatcher_id, name_called, patient_name, reason, adres, call_id,))
            else:
                cursor.execute('''SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS');''')
                date_time_call_close = cursor.fetchall()
                date_time_call_close = date_time_call_close[0][0]
                date_format = "%Y-%m-%d %H:%M:%S"
                date_time_call_close = datetime.strptime(date_time_call_close, date_format)
                cursor.execute('''update calls set call_dispatcher_id = %s, call_status_id = %s, full_name_call = %s, full_name_patient = %s,
                reason = %s, call_adres  = %s, time_call_close = %s where call_id = %s;''',
                              (dispatcher_id, 2, name_called, patient_name, reason, adres, date_time_call_close, call_id,))
        else:
            cursor.execute('''update calls set call_dispatcher_id = %s, full_name_call = %s, full_name_patient = %s,
            reason = %s, call_adres  = %s where call_id = %s;''',
                  (dispatcher_id, name_called, patient_name, reason, adres, call_id,))

        connect.commit()

        n_brigades = {item.split(',')[0] for item in new_selected_brigades}
        delete_brigades = [arr for arr in selected_brigades if arr.split(',')[0] not in n_brigades]#массив на удаление

        for i in range(len(delete_brigades)):
            brigade_id = delete_brigades[i].split(',', 1)[0].strip()
            cursor.execute('delete from brigades_calls where bc_call_id = %s and bc_brigade_id = %s;',
                           (call_id, brigade_id)) #удаление бригады с вызова

        for i in range(len(new_selected_brigades)):
            brigade_id = new_selected_brigades[i].split(',', 1)[0].strip()
            departure_times[i] = check_str(departure_times[i])
            arrival_times[i] = check_str(arrival_times[i])
            closure_times[i] = check_str(closure_times[i])
            if(new_selected_brigades[i] in selected_brigades):#бригада уже имееется на вызове(редактирование)
                cursor.execute('update brigades_calls set bc_exit = %s, bc_come = %s, bc_return = %s where bc_call_id = %s AND bc_brigade_id = %s;',
                (departure_times[i], arrival_times[i], closure_times[i], call_id, brigade_id,))
            else:#бригады нет на вызове (добавление новой записи)
                cursor.execute('INSERT INTO brigades_calls (bc_call_id, bc_brigade_id, bc_exit, bc_come, bc_return)''VALUES (%s, %s, %s, %s, %s);',
                               (call_id, brigade_id, departure_times[i], arrival_times[i], closure_times[i],))



        connect.commit()
        cursor.close()
        connect.close()

        return redirect(url_for('index'))

    return render_template('edit_call.html', brigades=brigades, selected_brigades=selected_brigades, Departure_Times=departure_Times, Arrival_Times=Arrival_Times,
    Closure_Times=Closure_Times, name_called=name_called, patient_name=patient_name, reason=reason, adres=adres, dispatchers=dispatchers, selected_dispatcher = dispatcher)

def check_str(str):
    if (str ==''):
        return None
    else:
        return str

def check_arr(departure_times, arrival_times, closure_times):
    if len(departure_times) == 0:
        return 1
    for array in (departure_times, arrival_times, closure_times):
        if any(arr == '' for arr in array):
            return 1
    return 2

@app.route('/delete_call/<int:call_id>', methods=['GET'])
def delete_call(call_id):

    connect = connect_dbase()
    cursor = connect.cursor()

    cursor.execute("delete from brigades_calls where bc_call_id = %s", (call_id,))
    cursor.execute("delete from calls where call_id = %s", (call_id,))

    connect.commit()
    cursor.close()
    connect.close()

    return redirect(url_for('index'))