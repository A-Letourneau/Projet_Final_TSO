using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;

using System.Threading;

namespace ServerTest
{
    class Program
    {

        static void Main(string[] args)
        {
            Program main = new Program();
            main.server_start();  //starting the server

            Console.ReadLine();
        }

        TcpListener server = new TcpListener(IPAddress.Any, 9999);

        private void server_start()
        {
            server.Start();
            accept_connection();  //accepts incoming connections
        }

        private void accept_connection()
        {
            server.BeginAcceptTcpClient(handle_connection, server);  //this is called asynchronously and will run in a different thread
        }

        private void handle_connection(IAsyncResult result)  //the parameter is a delegate, used to communicate between threads
        {
            accept_connection();  //once again, checking for any other incoming connections
            TcpClient client = server.EndAcceptTcpClient(result);  //creates the TcpClient

            NetworkStream ns = client.GetStream();

            /* here you can add the code to send/receive data */

        }

    }
}