import os
import sys
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as bckend
import pickle
import time

#import rpy2 



def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    
    if db_file.count("/") == 0:
        os.chdir('/home/luca/workspace/DCS_HV/python/')
        print("path: ", os.getcwd())
        print(db_file)
    try:
        #conn = sqlite3.connect('/home/luca/workspace/DCS_HV/python/TILE_DCS_HV-May2017.sqlite')
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None



def select_channel(conn,channel,hvlist=(1,48),metric="sd",resolution=0.5):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :param channel: the channel to be selected
    :param hvlist: tuple containing start/end subchannel indexes
    :return: data     """
    start_idx = int(hvlist[0])
    end_idx = int(hvlist[1])
    cur = conn.cursor()
    cur.execute('SELECT * FROM CONDBR2_F0003_IOVS')
    col_names = [cn[0] for cn in cur.description]
    sql_col = col_names[2]+ ", " + col_names[3] + ", " + ", ".join(col_names[(start_idx + 8):(end_idx + 9)])
    var_names = sql_col.split(", ")
    
    #header = [col_names[2], col_names[3]]
    #header.extend(col_names[(start_idx + 8):(end_idx + 9)])
    

    cur.execute("SELECT {v} FROM CONDBR2_F0003_IOVS where CHANNEL_ID={chan}".format(v=sql_col, chan=channel))
    rows = cur.fetchall() #list of tuples
    
    data_matrix = np.array(rows)
    
    data_dict = {}
    knots_dict = {}
    for i in range(len(data_matrix[0])):
        data_dict[var_names[i]] = data_matrix [:,i]
        
        #knots = np.where( np.diff(data_dict[var_names[i]]) > np.std(data_dict[var_names[i]]) )[0]
        if var_names[i] != 'IOV_SINCE' and var_names[i] != 'IOV_UNTIL':
            if metric=="sd":
                knots = list(np.where( np.abs( np.diff(data_dict[var_names[i]]) ) > min(np.std(data_dict[var_names[i]]),resolution) )[0] + 1)
            elif metric=="iqr":
                iqr = np.subtract(*np.percentile(data_dict[var_names[i]], [75, 25]))
                knots = list(np.where( np.abs( np.diff(data_dict[var_names[i]]) ) > min(iqr,resolution) )[0] + 1)
            else:
                print("ERROR: metric measure not supported. Try standard deviation <sd> or interquartile range <iqr>")
            knots.insert(0,0)
            knots.append( len(data_dict[var_names[i]]) -1 )
            knots_dict[var_names[i]] = knots #np.array([0,knots, len(data_matrix)])
    #cur.execute("SELECT IOV_SINCE,IOV_UNTIL,HVOUT1,HVOUT2  from CONDBR2_F0003_IOVS where CHANNEL_ID=?",channel)
    
    return [data_dict, knots_dict]
    
    #row = cur.fetchone()
        
#    runstatus = np.genfromtxt('collisiontime.txt', names=True, dtype=None)
#    for line in runstatus:
#    for row in rows:
#    	    if row[0]>=line[0] and row[1]<=line[1] and line[2]=="ON":
#                print(row)




	#DeltaT=(row[1]-row[0])/1000000000
        #print row[0],DeltaT

@profile
def piecewise_reg(data,knots,channel,diagnostics=0):
    """ train the model using Nadaraya-Watson estimator 
    :param data: data dictionary
    :param knots: knots dictionary
    :param channel: knots dictionary
    :param diagnostics: whether to produce diagnostic plots or not
    :return: dictionary with couples [knot, pred_value]
    :return: dictionary with performance measures
    """
    
    
    pred_dict = {}
    performance_dict = {}
    keys=sorted(data.keys())
    
#    n_fig=1
#    n_subpolt=1
#    plt.figure(1)
    

    
    if diagnostics==1:
        pdf = bckend.PdfPages("./risultati_presentazione/diagnostic_hv_channel{}.pdf".format(channel))

#        pdf = bckend.PdfPages("./diagnostic_plots/diagnostic_plots_channel{}.pdf".format(channel))
#        pdf = bckend.PdfPages("./diagnostic_plots_2017/diagnostic_plots_channel{}.pdf".format(channel))
    
    for var in list(keys)[:-2]: #exclude t_min and t_max
        
        pred=[]
        pred_vec=np.zeros(len(data[var]))
        
        for i in range ( len( knots[var] ) -1 ):
            start = knots[var][i]
            end = knots[var][i+1] 
            pred.append( [knots[var][i+1] , np.mean(data[var][start:end])]  )
            if end== (len(data[var]) -1) :
                end +=1
            pred_vec[start:end]=np.mean(data[var][start:end])
        
        pred_dict[var] = pred
        perc_err = (data[var] - pred_vec)/(data[var]+.0001)
        performance_dict[var] = { "MAE" : np.mean(abs(data[var] - pred_vec)),
                                  "MSE" : np.mean((data[var] - pred_vec)**2),
                                  "MAX" : np.max(abs(data[var] - pred_vec)),
                                  "MPE" : np.mean(perc_err)}
        
        if diagnostics==1:
        
            xlab=np.asarray(data["IOV_SINCE"], dtype='datetime64[ns]')
            plt.figure(1)
    #        plt.figure(n_fig)
    #        plt.subplot(3,2,1*n_subpolt)
            plt.subplot(2,1,1)
            plt.subplots_adjust(top=0.92, bottom=0.15, left=0.15, right=0.95, hspace=0.25,wspace=0.35)
            plt.plot(xlab, data[var], 'bo', xlab, pred_vec, 'r^', markersize=5)
            plt.ylabel("Voltage")
            #plt.xlabel("Time")
    #        label = real_vs_pred.xaxis.get_major_ticks()[2].label
    #        label.set_orientation('vertical')
            plt.title("Real (blue) VS Predicted (red)", fontsize=8, fontweight="bold")
            plt.text(xlab[5], pred_vec[0]+1, var)
    #        plt.show()
            
    #        plt.subplot(3,2,2*n_subpolt)
            plt.subplot(2,1,2)
            plt.subplots_adjust(top=0.88, bottom=0.12, left=0.15, right=0.95, hspace=0.25,wspace=0.35)
            plt.plot(xlab, perc_err, 'gs', markersize=5)
            plt.ylabel("Percentage error")
            plt.xlabel("Time")
            plt.title("Percentage error over time", fontsize=8, fontweight="bold")
            
    #        n_fig += 1
    #        n_subpolt += 1
    #        if n_subpolt == 3:
    #            n_fig += 1
    #            n_subpolt=1
    #            plt.figure(n_fig)
            
            pdf.savefig(1)
            plt.close()
    
    


    
    # sample usage
    save_object(pred_dict, './risultati_presentazione/pred_dict_channel_{}.pkl'.format(channel))
    save_object(performance_dict, './risultati_presentazione/performance_dict_channel_{}.pkl'.format(channel))
    
    return pred_dict, performance_dict

    

def main():
    
    #database = "TILE_DCS_HV-May-Jul-2017.sqlite"
    
#    f = open("test.txt","w")
#    database = "/data_shared/CondDB_DCS/TILE_DCS_HV_2017.sqlite"
    database = "TILE_DCS_HV_2017.sqlite"
#    f.write("HELLO WORLD: starting right now")
#    f.write(database)
    # create a database connection
    conn = create_connection(database)
#    runstatus = np.genfromtxt('collisiontime.txt',  dtype=None)
#    f.write("connessione riuscita")
    
    if not os.path.exists('diagnostic_plots_2017'):
        os.mkdir('diagnostic_plots_2017')

    if not os.path.exists('results_2017'):
        os.mkdir('results_2017')
    
#    f.write("cartelle create")
    for channel in range(int(sys.argv[1]),int(sys.argv[2])):
    #channel='10'


#        f.write("Inizio ciclo:")
#        f.write("Channel: {}".format(channel))
#        
#        f.write("Start:")
#        f.write(sys.argv[1])
#        f.write("End:")
#        f.write(sys.argv[1])
#        f.write("")
#        print ("Start:")
#        print (int(sys.argv[1]))
#        print ("End:")
#        print (int(sys.argv[1]))
#        
        with conn:
            data_dict, knots_dict = select_channel(conn,channel)
        
        exec_time=[]
        start = time.time()
        piecewise_reg(data_dict,knots_dict,channel,diagnostics=0)
        end = time.time()
        
        exec_time.append(end-start)
        if channel==(int(sys.argv[2]) -1):
            print("AVERAGE RUNNING TIME PER CHANNEL:")
            print(np.mean(exec_time))
        
    #data = select_channel(conn,"1")
    #print(data)
    
#        file = open('pred_channel_{}.obj'.format(channel), 'w')
#        pickle.dump(result[0], file)
#        file.close()
#    file = open('res_channel{}.txt'.format(channel),"w")
#    for key in result.keys():
#        file.write(str(key))
#        file.write(str(result[key]))
#    file.close()
#    f.close()
 
if __name__ == '__main__':
    main()


 




# struttura della TABLE:
# CREATE TABLE "CONDBR2_F0003_IOVS" ( "OBJECT_ID" UNSIGNEDINT ,"CHANNEL_ID" UNSIGNEDINT ,"IOV_SINCE" ULONGLONG ,"IOV_UNTIL" ULONGLONG ,"USER_TAG_ID" UNSIGNEDINT ,"SYS_INSTIME" TEXT ,"LASTMOD_DATE" TEXT ,"ORIGINAL_ID" UNSIGNEDINT ,"NEW_HEAD_ID" UNSIGNEDINT ,"HVOUT1" FLOAT ,"HVOUT2" FLOAT ,"HVOUT3" FLOAT ,"HVOUT4" FLOAT ,"HVOUT5" FLOAT ,"HVOUT6" FLOAT ,"HVOUT7" FLOAT ,"HVOUT8" FLOAT ,"HVOUT9" FLOAT ,"HVOUT10" FLOAT ,"HVOUT11" FLOAT ,"HVOUT12" FLOAT ,"HVOUT13" FLOAT ,"HVOUT14" FLOAT ,"HVOUT15" FLOAT ,"HVOUT16" FLOAT ,"HVOUT17" FLOAT ,"HVOUT18" FLOAT ,"HVOUT19" FLOAT ,"HVOUT20" FLOAT ,"HVOUT21" FLOAT ,"HVOUT22" FLOAT ,"HVOUT23" FLOAT ,"HVOUT24" FLOAT ,"HVOUT25" FLOAT ,"HVOUT26" FLOAT ,"HVOUT27" FLOAT ,"HVOUT28" FLOAT ,"HVOUT29" FLOAT ,"HVOUT30" FLOAT ,"HVOUT31" FLOAT ,"HVOUT32" FLOAT ,"HVOUT33" FLOAT ,"HVOUT34" FLOAT ,"HVOUT35" FLOAT ,"HVOUT36" FLOAT ,"HVOUT37" FLOAT ,"HVOUT38" FLOAT ,"HVOUT39" FLOAT ,"HVOUT40" FLOAT ,"HVOUT41" FLOAT ,"HVOUT42" FLOAT ,"HVOUT43" FLOAT ,"HVOUT44" FLOAT ,"HVOUT45" FLOAT ,"HVOUT46" FLOAT ,"HVOUT47" FLOAT ,"HVOUT48" FLOAT ,"TEMP1" FLOAT ,"TEMP2" FLOAT ,"TEMP3" FLOAT ,"TEMP4" FLOAT ,"TEMP5" FLOAT ,"TEMP6" FLOAT ,"TEMP7" FLOAT , PRIMARY KEY("OBJECT_ID"), FOREIGN KEY("CHANNEL_ID") REFERENCES CONDBR2_F0003_CHANNELS("CHANNEL_ID") );
