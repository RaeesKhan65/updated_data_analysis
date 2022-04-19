CREATE TABLE QPdata( 
	key SERIAL PRIMARY KEY, 
	date VARCHAR(200), 
	data_id VARCHAR(200), 
	sig_data NUMERIC ARRAY, 
	ref_data NUMERIC ARRAY, 
	sample NUMERIC, 
	count_time NUMERIC, 
	reset_time NUMERIC, 
	avg NUMERIC, 
	threshold NUMERIC, 
	aom_delay NUMERIC, 
	mw_delay NUMERIC, 
	type VARCHAR(200), 
	start NUMERIC, 
	stepsize NUMERIC, 
	steps NUMERIC, 
	pts VARCHAR(300), 
	srs VARCHAR(300), 
	avgcount NUMERIC, 
	x_arr NUMERIC ARRAY, 
	sample_name VARCHAR(200), 
	nv_name VARCHAR(200), 
	waveguide VARCHAR(200),
	nv_depth VARCHAR(200),
	nv_counts VARCHAR(200),
	metadata VARCHAR(50000),
	exp VARCHAR(200),
	time_stamp TIMESTAMP );