import socket
#---------- Info -----------------------------------------------------------
Domain = input("Enter the Domain: ")
server = "whois.iana.org"
print()
#---------- The function ---------------------------------------------------
def sendAndReseave(Domain, server, prev_server):
    s = socket.socket()
    s.connect((server,43)) # to start the connection with the server, and the port number (it has to be : 43)
    s.send(bytes(Domain,"ascii")+ b'\r\n')
    res = b''

    while(True):    # this loop just to make sure that the recv() got the full message !!
        message = s.recv(4096) 
        if message == b'':
            break
        else :
            res = res + message
    
    output = res.decode('utf-8') # To get the ability to get split to work!! 
    to_get_the_new_whois = output.split() # this split to make us able to get the item we need!!
    # here we need to get the (whois) item, then take the next item as the mew server link and get the function to work again with the new server name ... 
    for i in to_get_the_new_whois: # this loop to get the (whois) from the list 
        if i == "whois:" or "Server:" in  i:   
            server = to_get_the_new_whois[to_get_the_new_whois.index(i)+1] # this line is when we get the (whois:) then take the next one in the list!! 
            print(server) # just for debuging
            if server == prev_server:
                break
            else:
                    prev_server = server
            
            s.close() # to close the connection, security purposes!! 

            result = sendAndReseave(Domain, server, prev_server)
            if result is not None:
                print(result) # the recersive place, here when we call the function again.. 
            return
            break # to break the loop if we found the (whois:)
            #should add a way to break the function if Abdulrahman say ......... 
        else:
            continue # to keep going throw the list if we did not find the (whois:) 
    s.close() # to close the connection, security purposes!! 
    return output  # the output

#------------------------------------------------------------------------------
result = sendAndReseave(Domain, server, "") # to call the function ..... 
if result is not None:
    print(result) 
    
