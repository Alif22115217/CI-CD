using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tiket
{
    public class Tiket
    {
        public string Nama { get; set; }
        public string NIK { get; set; }
        public string NomorTelepon { get; set; }
        public string NomorKartuVaksin { get; set; }
        public string AlamatRumah { get; set; }

        public void PrintDetails()
        {
            Console.WriteLine("Detail Pemesanan Tiket:");
            Console.WriteLine($"Nama: {Nama}");
            Console.WriteLine($"NIK: {NIK}");
            Console.WriteLine($"Nomor Telepon: {NomorTelepon}");
            Console.WriteLine($"Nomor Kartu Vaksin: {NomorKartuVaksin}");
            Console.WriteLine($"Alamat Rumah: {AlamatRumah}");
            Console.WriteLine("Rute Perjalanan: Ketapang - Gilimanuk");
            Console.WriteLine("Jenis Transportasi: Kapal Laut");
        }
    }
}
