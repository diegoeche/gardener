PRAGMA journal_mode = WAL;
CREATE INDEX sensor_data_measured_at_index ON sensor_data(measured_at);
CREATE INDEX sensor_data_sensor_id_index ON sensor_data(sensor_id);
