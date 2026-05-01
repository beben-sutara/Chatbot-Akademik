-- Seed data untuk Chatbot Akademik

-- FAQ data
INSERT INTO faqs (pertanyaan, jawaban, kategori) VALUES
('Bagaimana cara mengisi KRS?', 'Untuk mengisi KRS: 1) Login ke portal akademik 2) Pilih menu Pengisian KRS 3) Pilih mata kuliah yang tersedia sesuai semester 4) Konfirmasi dengan dosen wali 5) Submit sebelum batas waktu yang ditentukan.', 'registrasi'),
('Kapan batas waktu pengisian KRS?', 'Batas waktu pengisian KRS biasanya pada minggu pertama awal semester. Cek kalender akademik untuk tanggal pasti.', 'registrasi'),
('Bagaimana cara melihat nilai?', 'Anda dapat melihat nilai melalui: 1) Portal akademik mahasiswa 2) Fitur cek nilai di chatbot ini 3) Menghubungi bagian akademik secara langsung.', 'nilai'),
('Apa itu IPK dan bagaimana cara menghitungnya?', 'IPK (Indeks Prestasi Kumulatif) adalah rata-rata nilai semua mata kuliah yang sudah ditempuh. Dihitung dengan rumus: Jumlah (SKS x Bobot Nilai) / Total SKS.', 'nilai'),
('Bagaimana cara mengajukan cuti akademik?', 'Untuk mengajukan cuti akademik: 1) Unduh formulir cuti di portal akademik 2) Isi formulir dengan lengkap 3) Minta tanda tangan dosen wali 4) Serahkan ke bagian akademik 5) Tunggu persetujuan dari dekan.', 'administrasi'),
('Dimana kantor akademik berada?', 'Kantor Bagian Akademik berada di Gedung Rektorat Lantai 2. Jam operasional: Senin-Jumat 08.00-16.00 WIB.', 'informasi'),
('Bagaimana cara mengurus transkrip nilai?', 'Untuk mengurus transkrip nilai: 1) Datang ke kantor akademik 2) Isi formulir permohonan transkrip 3) Bayar biaya administrasi 4) Tunggu 3-5 hari kerja 5) Ambil transkrip di kantor akademik.', 'administrasi'),
('Apa syarat untuk mengambil skripsi?', 'Syarat mengambil skripsi: 1) Minimal 120 SKS lulus 2) IPK minimal 2.00 3) Tidak ada nilai E 4) Sudah mengambil mata kuliah metodologi penelitian 5) Mendapat persetujuan dosen wali.', 'akademik');

-- Academic calendar data
INSERT INTO academic_calendar (judul, deskripsi, tanggal_mulai, tanggal_selesai, kategori) VALUES
('Penerimaan Mahasiswa Baru', 'Proses penerimaan mahasiswa baru tahun akademik 2025/2026', '2025-07-01', '2025-08-15', 'penerimaan'),
('Registrasi Mahasiswa Baru', 'Registrasi dan orientasi mahasiswa baru', '2025-08-18', '2025-08-22', 'registrasi'),
('Pengisian KRS Semester Ganjil', 'Periode pengisian KRS untuk semester ganjil 2025/2026', '2025-08-25', '2025-09-05', 'krs'),
('Kuliah Semester Ganjil Dimulai', 'Awal perkuliahan semester ganjil 2025/2026', '2025-09-08', NULL, 'perkuliahan'),
('Ujian Tengah Semester (UTS)', 'Periode Ujian Tengah Semester Ganjil 2025/2026', '2025-11-03', '2025-11-14', 'ujian'),
('Ujian Akhir Semester (UAS)', 'Periode Ujian Akhir Semester Ganjil 2025/2026', '2026-01-05', '2026-01-16', 'ujian'),
('Pengumuman Nilai Semester Ganjil', 'Pengumuman hasil nilai ujian semester ganjil', '2026-01-26', NULL, 'nilai'),
('Pengisian KRS Semester Genap', 'Periode pengisian KRS untuk semester genap 2025/2026', '2026-02-02', '2026-02-13', 'krs'),
('Kuliah Semester Genap Dimulai', 'Awal perkuliahan semester genap 2025/2026', '2026-02-16', NULL, 'perkuliahan'),
('Wisuda Periode I', 'Wisuda periode pertama tahun 2026', '2026-04-25', NULL, 'wisuda');

-- Sample courses
INSERT INTO courses (kode_mk, nama_mk, sks, semester, deskripsi) VALUES
('CS101', 'Pengantar Ilmu Komputer', 3, 1, 'Mata kuliah pengantar yang membahas konsep dasar ilmu komputer'),
('CS102', 'Algoritma dan Pemrograman', 4, 1, 'Pemrograman dasar menggunakan Python'),
('CS201', 'Struktur Data', 3, 2, 'Konsep dan implementasi struktur data'),
('CS202', 'Basis Data', 3, 3, 'Desain dan implementasi basis data relasional'),
('CS301', 'Rekayasa Perangkat Lunak', 3, 5, 'Metodologi pengembangan perangkat lunak'),
('CS401', 'Kecerdasan Buatan', 3, 7, 'Konsep dan aplikasi kecerdasan buatan'),
('MATH101', 'Kalkulus I', 3, 1, 'Limit, turunan, dan integral'),
('MATH201', 'Aljabar Linear', 3, 2, 'Vektor, matriks, dan transformasi linear');
