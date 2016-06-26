#!/usr/bin/python3

import http.client;
import argparse
import json

#$.ajax({ url:url, type:"POST", data:JSON.stringify({"frequency":frequency, "preamble":"", "irCode":ircode, "repeat":"1"}), contentType:"application/json", crossDomain : true});

def call_itach(host, frequency, ircode, repeat):
    headers = { 'Content-Type': 'application/json' }
    json_request_object = {"frequency":frequency, "preamble":"", "irCode":ircode, "repeat": repeat}
    json_request = json.dumps(json_request_object)
    
    print(json_request)

    httpRequest = http.client.HTTPConnection(host, 80)
    httpRequest.request("POST", '/api/v1/irports/3/sendir', json_request, headers)
    response = httpRequest.getresponse()
    httpRequest.close()
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a message to an iTach.')
    parser.add_argument('-H', dest='host', help='IP address or hostname', required=True)
    parser.add_argument('-f', dest='frequency', type=int, required=True)
    parser.add_argument('-i', dest='ircode', required=True)
    parser.add_argument('-r', dest='repeat', type=int, default=1)

    args = parser.parse_args();
    
    call_itach(args.host, args.frequency, args.ircode, args.repeat)
