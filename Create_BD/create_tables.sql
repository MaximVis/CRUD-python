DO $$
BEGIN

create table if not exists ranks(

	rank_id integer NOT NULL,
	rank_name text NOT NULL,
	constraint rank_pk primary key(rank_id)
	
);

create table if not exists dispatchers(

	dispatcher_id integer NOT NULL,
	full_name text NOT NULL,
	constraint dispatcher_pk primary key(dispatcher_id)
	
);

create table if not exists status_calls(

	status_call_id integer NOT NULL,
	status_call text NOT NULL,
	constraint status_call_pk primary key(status_call_id)
);

create table if not exists status_brigades(

	status_brigade_id integer NOT NULL,
	status_brigade text NOT NULL,
	constraint status_brigade_pk primary key(status_brigade_id)
);

create table if not exists works_timetable(--график работы_бригады

	work_timetable_id integer NOT NULL,
	time_duty_start time NOT NULL,
	time_duty_end time NOT NULL,
	constraint work_timetable_pk primary key(work_timetable_id)
);

create table if not exists stations(

	station_id integer NOT NULL,
	adress text NOT NULL,
	district text NOT NULL,
	constraint station_pk primary key(station_id)

);

create table if not exists ambulances(
	
	ambulance_id integer NOT NULL,
	ambulance_station_id integer NOT NULL,
	state_number text NOT NULL,
	constraint ambulance_pk primary key (ambulance_id)
	
);

create table if not exists employees_members(
	
	employee_id integer NOT NULL,
	employee_station_id integer NOT NULL,
	employee_rank_id integer NOT NULL,
	full_name text NOT NULL,
	constraint employee_pk primary key(employee_id)
	
);

create table if not exists calls(

	call_id serial NOT NULL,
	call_dispatcher_id integer NOT NULL,
	call_status_id integer NOT NULL,
	date_time_call timestamp NOT NULL,
	time_call_accept timestamp NOT NULL,
	full_name_call text,
	full_name_patient text,
	reason text NOT NULL,
	call_adres text NOT NULL,
	time_call_close timestamp,
	constraint call_pk primary key(call_id)
	
);

create table if not exists brigades(

	brigade_id integer NOT NULL,
	brigade_doctor_id integer NOT NULL,
	brigade_paramedic_id integer NOT NULL,
	brigade_driver_id integer NOT NULL,
	brigade_work_timetable_id integer NOT NULL,
	brigade_status_id integer NOT NULL,
	brigade_ambulance_id integer NOT NULL,
	brigade_location text NOT NULL,
	date_duty date NOT NULL,
	constraint brigade_pk primary key(brigade_id)
);

create table if not exists brigades_calls(

	bc_id serial NOT NULL,
	bc_call_id integer NOT NULL,
	bc_brigade_id integer NOT NULL,
	bc_exit time,
	bc_come time,
	bc_return time,
	constraint bc_pk primary key(bc_id)
);

END$$;













