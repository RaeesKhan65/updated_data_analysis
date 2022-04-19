import psycopg2 as pg2

def decorator_extract(original_function):
    """

This function is a decorator for any function that would extract data
into the DB and is designed in the Query/Content



|
    """

    def wrapper_function(*args, **kwargs):
        a, b, c = original_function(*args, **kwargs)
        conn = pg2.connect(database= 'duttlab', user='postgres', password='Duttlab')
        cur = conn.cursor()
        executable = cur.mogrify(a,b)
        cur.execute(executable)
        data = cur.fetchall()
        conn.close()

        if(c == "quantumpulse"):
            return unpack_data_qp(data)

        elif(c=="rb"):
            return unpack_data_rb(data)

        else:
            return -1

    return wrapper_function

@decorator_extract
def extract_data_qp(date = None, data_id = None, key = None, sample = None, count_time = None, reset_time = None,
                 avg = None, threshold = None, aom_delay = None, mw_delay = None,
                 Type = None, start = None, stepsize = None, steps = None, avgcount = None,
                 pts = None,srs = None, sample_name = None, nv_name = None, waveguide = None, nv_depth = None,nv_counts = None):

    """
            This function is used to extract Quantum pulse data from the SQL DB.

            :param: Takes inputs of what you want to search.
            :type: string,list
            :rtype: list
            :return: returns data object.

            |


    """
    if(date != None):
        date = date + '%'


    if(data_id != None):
        data_id = data_id + '%'

    content = []
    input = [date,data_id,key,sample,count_time,reset_time,avg,threshold,aom_delay,mw_delay,Type,
             start,stepsize,steps,avgcount,pts,srs,sample_name,nv_name,waveguide,nv_depth,nv_counts]


    input_strings = [" date LIKE %s"," and data_id LIKE %s"," and key = %s"," and sample = %s"," and count_time = %s",
                     " and reset_time = %s"," and avg = %s"," and threshold = %s",
                     " and aom_delay = %s"," and microwave_delay = %s"," and Type = %s",
                     " and start = %s"," and stepsize = %s"," and steps = %s"," and avgcount = %s",
                     " and pts = %s"," and srs = %s"," and sample_name = %s", " and nv_name = %s",
                     " and waveguide = %s", " and nv_depth = %s", " and nv_counts = %s"]

    query = 'SELECT * FROM QPdata WHERE'
    val = True

    for i,j in enumerate(input):

        if(j!=None):
            if(input[0]==None and val == True):
                query = query + input_strings[i][4:]
                content.append(j)
                val = False
                continue
            content.append(j)
            query = query + input_strings[i]

    if(query == 'SELECT * FROM QPdata WHERE'):

        query = 'SELECT * FROM QPdata WHERE exp = %s'
        content.append("quantumpulse")

    return (query, content, "quantumpulse")

@decorator_extract
def extract_data_rb(date = None, data_id = None, key = None, sample = None, count_time = None, reset_time = None,
                    avg = None, threshold = None, aom_delay = None, mw_delay = None,
                    Type = None, start = None, stepsize = None, steps = None, avgcount = None,
                    pts = None,srs = None, sample_name = None, nv_name = None, waveguide = None, nv_depth = None,nv_counts = None):

    """
            This function is used to extract Randomized Benchmarking data from the SQL DB.

            :param: Takes inputs of what you want to search.
            :type: string,list
            :rtype: list
            :return: returns data object.

            |


    """
    if(date != None):
        date = date + '%'


    if(data_id != None):
        data_id = data_id + '%'

    content = []
    input = [date,data_id,key,sample,count_time,reset_time,avg,threshold,aom_delay,mw_delay,Type,
             start,stepsize,steps,avgcount,pts,srs,sample_name,nv_name,waveguide,nv_depth,nv_counts]


    input_strings = [" date LIKE %s"," and data_id LIKE %s"," and key = %s"," and sample = %s"," and count_time = %s",
                     " and reset_time = %s"," and avg = %s"," and threshold = %s",
                     " and aom_delay = %s"," and microwave_delay = %s"," and Type = %s",
                     " and start = %s"," and stepsize = %s"," and steps = %s"," and avgcount = %s",
                     " and pts = %s"," and srs = %s"," and sample_name = %s", " and nv_name = %s",
                     " and waveguide = %s", " and nv_depth = %s", " and nv_counts = %s"]

    query = 'SELECT * FROM RBdata WHERE'
    val = True

    for i,j in enumerate(input):

        if(j!=None):
            if(input[0]==None and val == True):
                query = query + input_strings[i][4:]
                content.append(j)
                val = False
                continue
            content.append(j)
            query = query + input_strings[i]

    if(query == 'SELECT * FROM RBdata WHERE'):

        query = 'SELECT * FROM RBdata WHERE exp = %s'
        content.append("rb")

    return (query, content, "rb")

class unpack_data_qp: #List of all the accesible attributes
    def __init__(self, data):
        self.key = [row[0] for row in data]
        self.date = [row[1] for row in data]
        self.data_id = [row[2] for row in data]
        self.sig_data = [row[3] for row in data]
        self.ref_data = [row[4] for row in data]
        self.sample = [row[5] for row in data]
        self.count_time = [row[6] for row in data]
        self.reset_time = [row[7] for row in data]
        self.avg = [row[8] for row in data]
        self.threshold = [row[9] for row in data]
        self.aom_delay = [row[10] for row in data]
        self.mw_delay = [row[11] for row in data]
        self.type = [row[12] for row in data]
        self.start = [row[13] for row in data]
        self.stepsize = [row[14] for row in data]
        self.steps = [row[15] for row in data]
        self.pts = [row[16] for row in data]
        self.srs = [row[17] for row in data]
        self.avgcount = [row[18] for row in data]
        self.x_arr = [row[19] for row in data]
        self.sample_name = [row[20] for row in data]
        self.nv_name = [row[21] for row in data]
        self.waveguide = [row[22] for row in data]
        self.nv_depth = [row[23] for row in data]
        self.nv_counts = [row[24] for row in data]
        self.metadata = [row[25] for row in data]
        self.exp = [row[26] for row in data]
        self.time_stamp = [row[27] for row in data]


class unpack_data_rb: #List of all the accesible attributes
    def __init__(self, data):
        self.key = [row[0] for row in data]
        self.date = [row[1] for row in data]
        self.data_id = [row[2] for row in data]
        self.sig_data = [row[3] for row in data]
        self.ref_data = [row[4] for row in data]
        self.sample = [row[5] for row in data]
        self.count_time = [row[6] for row in data]
        self.reset_time = [row[7] for row in data]
        self.avg = [row[8] for row in data]
        self.threshold = [row[9] for row in data]
        self.aom_delay = [row[10] for row in data]
        self.mw_delay = [row[11] for row in data]
        self.type = [row[12] for row in data]
        self.start = [row[13] for row in data]
        self.stepsize = [row[14] for row in data]
        self.steps = [row[15] for row in data]
        self.pts = [row[16] for row in data]
        self.srs = [row[17] for row in data]
        self.avgcount = [row[18] for row in data]
        self.x_arr = [row[19] for row in data]
        self.sample_name = [row[20] for row in data]
        self.nv_name = [row[21] for row in data]
        self.waveguide = [row[22] for row in data]
        self.nv_depth = [row[23] for row in data]
        self.nv_counts = [row[24] for row in data]
        self.lengths = [row[25] for row in data]
        self.final_states = [row[26] for row in data]
        self.metadata = [row[27] for row in data]
        self.exp = [row[28] for row in data]
        self.time_stamp = [row[29] for row in data]