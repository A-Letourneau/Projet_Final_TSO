using System;
using System.Net;
using System.Net.Sockets;
using System.Configuration;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Projet_Final_Preparation_UDP
{
    public partial class Form1 : Form
    {
        const int listenPort = 4210;

        public Form1()
        {
            InitializeComponent();
            
        }

        private void btn_Confirm_Click(object sender, EventArgs e)
        {
            string ipADR = textBox_IP_ADR.Text;
            
        }

        private void btn_listen_Click(object sender, EventArgs e)
        {

        }

        private void btn_send_Click(object sender, EventArgs e)
        {

        }
    }
}
