using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tiket
{
    public class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Selamat datang di Ferizy");
            Console.WriteLine("Silakan masukkan data anda untuk pemesanan tiket:");

            Tiket tiket = new Tiket()

            Console.Write("Nama: ");
            tiket.Nama = Console.ReadLine();

            Console.Write("NIK: ");
            tiket.NIK = Console.ReadLine();

            Console.Write("Nomor Telepon: ");
            tiket.NomorTelepon = Console.ReadLine();

            Console.Write("Nomor Kartu Vaksin: ");
            tiket.NomorKartuVaksin = Console.ReadLine();

            Console.Write("Alamat Rumah: ");
            tiket.AlamatRumah = Console.ReadLine();

            Console.WriteLine();
            tiket.PrintDetails();

            Console.WriteLine("Terima kasih telah melakukan pemesanan tiket. Selamat menikmati perjalanan!");
        }
    }
}
