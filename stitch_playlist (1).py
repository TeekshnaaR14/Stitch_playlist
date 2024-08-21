import shutil
import mysql.connector
import csv
import os
import subprocess
import glob



# take user inputs
print("")
passid = input("Enter SkillTeck ID : ")

# check if both inputs are provided
if passid == "" :
    print(" Input (SkillTeck ID) is required. Exiting.")
    exit()

# convert integer input to int type
try:
    passid = int(passid)
except ValueError:
    print("SkillTeck ID input must be an integer. Exiting.")
    exit()


choice = input("\n" "Is the correct SkillTeck ID ...  Do you want to continue (Yes/No)? ")

# check user choice
if choice.lower() == 'yes':

    try:
        connection = mysql.connector.connect(host='skillteck-test-db.cbhiix7ahnlk.us-west-1.rds.amazonaws.com',
                                             database='skillteck-phase2',
                                             user='skillteck_test',
                                             password='70Z89Q7Dhcfz0wzf5Pdt')


        cursor = connection.cursor()
        sql_select_Query = "select CONCAT(firstName, ' ' ,lastName) as fl_name, id from users where id = %s"

#        passid = input("Enter SkillTeck ID : ")
#        pass_pl_id = input("Enter PlayList ID : ")
        cursor.execute(sql_select_Query, (passid,))
        # get all records
        records = cursor.fetchall()

        if cursor.rowcount == 0:
           print(" No matching SkillTeck ID..existing ..")
           exit()
        elif cursor.rowcount >= 2:
           print(" Multiple matching SkillTeck ID..existing ..")
           exit()
        else:
    #        print("\nPrinting each row")
            for row in records:
                print("\n" "SkillTeck Id  = ", row[1])
                print("FirstName, LastName = ", row[0], "\n")
                fpassid = row[1]
                fpassid_fl = row[0]


        sql_select_Query = "select Id, name from playlists where userid = %s order by createdAt desc LIMIT 10"
        cursor.execute(sql_select_Query, (passid,))
        # get all records
        records = cursor.fetchall()

        if cursor.rowcount == 0:
           print(" No matching Playlist ID..existing ..")
           exit()
#        elif cursor.rowcount >= 2:
#           print(" Multiple matching Playlist ID..existing ..")
#           exit()
        else:
            id_list = []
            print("List of Playlist ID and Name")
            print("===========================================")
            for row in records:
                print("Playlist ID and Name -> ", row[0], row[1], )
                fpass_pl_id = row[0]
                fpass_pl_id_n = row[1]
                id_list.append(row[0])
        print("===========================================")
#        print(id_list)
        pass_pl_id = int(input("Enter PlayList ID : "))
#        print(" My playlist to rubn : ", pass_pl_id)

        if pass_pl_id in id_list:
#            print("Value found in results!")

            sql_select_Query = "select name from playlists where id = %s "
            cursor.execute(sql_select_Query, (pass_pl_id,))
            records = cursor.fetchall()
            for row in records:
                pass_pl_name = row[0]
#                print("Group Name -> here inside")
#                print("Group Name -> ", fpass_gp_name )

            print("\n" "********************************************************************************" "\n")
            sql_select_Query = "select Id, name from `groups` where createdby = %s order by createdAt desc LIMIT 10"
            cursor.execute(sql_select_Query, (passid,))
            # get all records
            records = cursor.fetchall()

            if cursor.rowcount == 0:
               print(" No matching groups ID..existing ..")
               exit()
    #        elif cursor.rowcount >= 2:
    #           print(" Multiple matching Playlist ID..existing ..")
    #           exit()
            else:
                id_gp_list = []
                print("\n" "List of Group ID and Name")
                print("===========================================")
                for row in records:
                    print("Group ID and Name -> ", row[0], row[1], )
                    fpass_gp_id = row[0]
                    fpass_gp_id_n = row[1]
                    id_gp_list.append(row[0])
            print("===========================================")
#            print(id_gp_list)
            pass_gp_id = int(input("Enter Group ID : "))
            sql_select_Query = "select Id, name from `groups` where id = %s"
            cursor.execute(sql_select_Query, (pass_gp_id,))
            records = cursor.fetchall()
#            print("Group Name -> here ")
            for row in records:
                pass_gp_name = row[1]
#                print("Group Name -> here inside")
#                print("Group Name -> ", fpass_gp_name )

            print("\n" "********************************************************************************" "\n")

            print("Final Input Validation" "\n")
            print("SkillTeck Id         : " , fpassid)
            print("FirstName, LastName  : ", fpassid_fl)
            print("\n" "Playlist ID     : ", pass_pl_id)
            print("\n" "Group ID     : ", pass_gp_id)
#            print("\n" "===============================================================" "\n")
            print("\n" "********************************************************************************" "\n")

            fchoice = input("Is all above information correct ... Are you sure (Yes/No)? ")
            # check user choice
            if fchoice.lower() == 'yes':

                dirpath = 'Downloads/' + str(passid) + '/' + str(pass_pl_id)
                if os.path.exists(dirpath):
                    shutil.rmtree(dirpath)
                    os.makedirs(dirpath)
                else:
                    os.makedirs(dirpath)



                curdir = os.getcwd()
                mylistname = 'download_list.sh'
                formatted_stitchfile = 'ready_for_ffmpeg.txt'
                stitchname_exec = 'create_stich_format.sh'
                finalupload_exec = 'run_stich_and_upload.sh'
                smsseconds_exec = 'get_sms_clips_in_seconds.sh'
                sms_data_in_seconds = 'sms_data.txt'
                dlfilename = dirpath + '/' + mylistname
                exec_file = curdir + '/' + dlfilename
                dl_dir = curdir + '/' + dirpath
                rm_old_files = dl_dir + '/*.mp4'
                file_to_stick = dl_dir + '/' + stitchname_exec
                final_stick_upload = dl_dir + '/' + finalupload_exec
                file_to_sms_seconds = dl_dir + '/' + smsseconds_exec
                data_in_sms_seconds = dl_dir + '/' + sms_data_in_seconds
                concat_id_playid = '%' + str(passid) + '_' + str(pass_pl_id) + '%'
            #    print(rm_old_files)
            #    print(dlfilename)
            #    print(exec_file)
            #    print(dl_dir)


                dbQuery = '''SELECT CONCAT(REPLACE(L.media,'https://skillteck-v2.s3.us-west-1.amazonaws.com/videos/', 'aws s3 cp s3://skillteck-v2/videos/'),' ', CONCAT(TRIM(' ' FROM L.id),'.mp4')) as data
                                FROM  library_medias L
                                WHERE L.playlistId = (
                                                    SELECT P.ID FROM playlists P WHERE
                                                    P.userId = (SELECT ID FROM users u WHERE id=%s)
                                                    AND id = %s)
                                AND mediaType = '2'
                                AND media not like %s
                                ORDER BY createdAt ASC'''

                cur=connection.cursor()
                pass_var = (passid, pass_pl_id, concat_id_playid)
                cur.execute(dbQuery, pass_var)
                rows=cur.fetchall()
                if cur.rowcount == 0:
                   print(" No MP4 clips for SkillTeck ID " + passid + " ..existing ..")
                   exit()
            #    column_names = [i[0] for i in cur.description]
                fp = open(dlfilename, 'w')
                myFile = csv.writer(fp, lineterminator = '\n')
            #        myFile.writerow(column_names)
                myFile.writerows(rows)
                fp.close()

            ### Downloading mp4 clips to local directory
                subprocess.call(['chmod', '755', dlfilename])
                os.chdir(dl_dir)
                P = subprocess.Popen(['sh', exec_file])
                P.wait()
                print("All MP4 clips are downloaded  Successfully !!!")
                print(" ")
                print("Group ID -> ", pass_gp_id )
                print("Group Name -> ", pass_gp_name )

            ### Creating file for ffmpeg format for consolidated final stitch
                output_file = open(file_to_stick, "w")
                call_in_sh = "for f in *.mp4; do echo " """ "file '$f'" """ ">> " + formatted_stitchfile + "; done \n"
                output_file.writelines(call_in_sh)
                output_file.close()

                subprocess.call(['chmod', '755', file_to_stick])
                P = subprocess.Popen(['sh', file_to_stick])
                P.wait()
                print("...... Stitch formatted ready_for_ffmpeg.txt file is readnew.pyy !!!")
                print(" ")

            #### Creating final ffmpeg commands to upload to S3 bucket
                output_file = open(final_stick_upload, "w")
                add_line1 = "ffmpeg -f concat -safe 0 -i " + formatted_stitchfile + " -c copy " + str(passid) + "_" + str(pass_pl_id) + ".mp4 \n"
                add_line2 = "aws s3 cp " + str(passid) + "_" + str(pass_pl_id) + ".mp4 s3://skillteck-v2/videos/" + str(passid) + "/library/" + str(passid) + "_" + str(pass_pl_id) + ".mp4 \n"
                output_file.writelines(add_line1)
                output_file.writelines(add_line2)
                output_file.close()

            ### Executing the shell script to upload to S3 ....it might take few minutes to finish
                subprocess.call(['chmod', '755', final_stick_upload])
                P = subprocess.Popen(['sh', final_stick_upload])
                P.wait()
                print("file stitched and uploaded to S3 successfully !!!")
                print(" ")




            ### Finding total sms clips timing in seconds
                output_file = open(file_to_sms_seconds, "w")
                call_in_sh = "mplayer -identify -frames 0 -vo null -nosound " + str(passid) + "_" + str(pass_pl_id) + ".mp4 2>&1 | awk -F= '/LENGTH/{print $2}'| cut -f1 -d'.' > " + data_in_sms_seconds + " \n"
            #    print("mmmm : %s" % call_in_sh)
                output_file.writelines(call_in_sh)
                output_file.close()

                subprocess.call(['chmod', '755', file_to_sms_seconds])
                P = subprocess.Popen(['sh', file_to_sms_seconds])
                P.wait()
                print("...... get_sms_clips_in_seconds.sh executed  !!!")

                output_file = open(data_in_sms_seconds, "r")
                pass_seconds = output_file.readline()
                output_file.close()

                pass_media = "https://skillteck-v2.s3.us-west-1.amazonaws.com/videos/" + str(passid) + "/library/" + str(passid) + "_" + str(pass_pl_id) + ".mp4"
                pass_mediatype = 2
                pass_mediaThumbnail = "https://skillteck-v2.s3.us-west-1.amazonaws.com/videos/smspic.jpg"

            #    print(" used id : %s" % passid)
                print("pass_media : %s" % pass_media)
            #    print("pass_mediatype : %s" % pass_mediatype)
                print("pass_mediaThumbnail : %s" % pass_mediaThumbnail)
            #    print("pass_seconds real : %s" % pass_seconds)
            #    print("pass_seconds fixed : %s" % var_sec)
            #    print("playlistId : %s" %pass_pl_id)


                del_sql = "DELETE FROM library_medias  where media = %s"
                del_pass_many_var = (pass_media)
                cursor.execute(del_sql, (del_pass_many_var,))
                connection.commit()

            ### inserting sql statement for final link for customer to play
#                ins_sql = "INSERT INTO library_medias (userId, media, mediaType, mediaThumbnail, seconds, playlistId, createdAt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#                pass_many_var = (passid, pass_media, pass_mediatype, pass_mediaThumbnail, pass_seconds, pass_pl_id,'2021-07-03')
                ins_sql = "INSERT INTO library_medias (userId, media, mediaType, mediaThumbnail, seconds, playlistId) VALUES (%s, %s, %s, %s, %s, %s)"
                pass_many_var = (passid, pass_media, pass_mediatype, pass_mediaThumbnail, pass_seconds, pass_pl_id)
                cur.execute(ins_sql, pass_many_var)
                connection.commit()

                del_sql = "DELETE FROM showcases where gamename = %s"
                del_pass_many_var = (pass_pl_name)
                cursor.execute(del_sql, (del_pass_many_var,))
                connection.commit()

                sql_select_Query = "select userId from group_members where groupId = %s"
                cursor.execute(sql_select_Query, (pass_gp_id,))
                records = cursor.fetchall()

                for row in records:
                    pass_show_userid = row[0]
                    print("Showcase user list id  -> ", pass_show_userid )
                    ins_sql = "INSERT INTO showcases  (userId, Image, gamename, url, type ) VALUES (%s, %s, %s, %s, %s)"
                    pass_many_var = (pass_show_userid, 'showcaseImage/59486e4c-e8cb-4c5f-a13e-f7ac5356fafd.jpeg', pass_pl_name, pass_media,'stats')
                    cur.execute(ins_sql, pass_many_var)
                    connection.commit()
                
                print(" ")
                print("All Done successfully")
                shutil.rmtree(dl_dir)
            else:
                print('Value not found in results.')
                print(" Just Relalised this is not one to stitch videos ...whoops    .....existing ..")
                shutil.rmtree(dl_dir)

        else:
            print(" No matching Playlist ID and it is not in above list either ..existing ..")
            exit()



    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print(" .... MySQL connection is closed")

elif choice.lower() == 'no':
    print(" Just Relalised incorrect SkillTeck ID entered whoops    .....existing ..")
    exit()
else:
    print("Invalid choice. Please enter 'yes' or 'no' in upper or lower case.")
    exit()


