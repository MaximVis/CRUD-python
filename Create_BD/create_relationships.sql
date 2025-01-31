DO $$
BEGIN


ALTER TABLE calls
ADD CONSTRAINT call_FK1 FOREIGN KEY (call_dispatcher_id)
REFERENCES dispatchers(dispatcher_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE calls
ADD CONSTRAINT call_FK2 FOREIGN KEY (call_status_id)
REFERENCES status_calls(status_call_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE ambulances
ADD CONSTRAINT ambulance_FK1 FOREIGN KEY (ambulance_station_id)
REFERENCES stations(station_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE employees_members
ADD CONSTRAINT employee_FK1 FOREIGN KEY (employee_station_id)
REFERENCES stations(station_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE employees_members
ADD CONSTRAINT employee_FK2 FOREIGN KEY (employee_rank_id)
REFERENCES ranks(rank_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE brigades
ADD CONSTRAINT brigade_FK1 FOREIGN KEY (brigade_doctor_id)
REFERENCES employees_members(employee_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE brigades
ADD CONSTRAINT brigade_FK2 FOREIGN KEY (brigade_paramedic_id)
REFERENCES employees_members(employee_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE brigades
ADD CONSTRAINT brigade_FK3 FOREIGN KEY (brigade_driver_id)
REFERENCES employees_members(employee_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE brigades
ADD CONSTRAINT brigade_FK4 FOREIGN KEY (brigade_work_timetable_id)
REFERENCES works_timetable(work_timetable_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE brigades
ADD CONSTRAINT brigade_FK5 FOREIGN KEY (brigade_status_id)
REFERENCES status_brigades(status_brigade_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE brigades
ADD CONSTRAINT brigade_FK6 FOREIGN KEY (brigade_ambulance_id)
REFERENCES ambulances(ambulance_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE brigades_calls
ADD CONSTRAINT bc_FK1 FOREIGN KEY (bc_call_id)
REFERENCES calls(call_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE brigades_calls
ADD CONSTRAINT bc_FK2 FOREIGN KEY (bc_brigade_id)
REFERENCES brigades(brigade_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


END$$

















