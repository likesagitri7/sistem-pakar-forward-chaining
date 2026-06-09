-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 03, 2026 at 01:24 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_maternal`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_admin`
--

CREATE TABLE `tb_admin` (
  `id_admin` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_admin`
--

INSERT INTO `tb_admin` (`id_admin`, `username`, `password`, `nama_lengkap`) VALUES
(1, 'admin', 'admin123', 'Administrator'),
(3, 'pakar_dr.Ade', 'pakar123', 'dr. Ade Aulia, Sp.OG'),
(6, 'IT_Like', 'like123', 'Like Sagitri Helen');

-- --------------------------------------------------------

--
-- Table structure for table `tb_aturan`
--

CREATE TABLE `tb_aturan` (
  `id_aturan` int(11) NOT NULL,
  `kode_rule` varchar(5) DEFAULT NULL,
  `kode_penyakit` varchar(10) DEFAULT NULL,
  `detail_kondisi` text DEFAULT NULL,
  `kode_gejala` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_aturan`
--

INSERT INTO `tb_aturan` (`id_aturan`, `kode_rule`, `kode_penyakit`, `detail_kondisi`, `kode_gejala`) VALUES
(1, 'R1', 'P01', 'Hipertensi dalam Kehamilan (Preeklamsia Ringan)', 'G26'),
(2, 'R1', 'P01', 'Hipertensi dalam Kehamilan (Preeklamsia Ringan)', 'G28'),
(3, 'R1', 'P01', 'Hipertensi dalam Kehamilan (Preeklamsia Ringan)', 'G04'),
(4, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G26'),
(5, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G29'),
(6, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G01'),
(7, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G02'),
(8, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G03'),
(9, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G31'),
(10, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G14'),
(11, 'R2', 'P02', 'Hipertensi dalam Kehamilan (Preeklamsia Berat)', 'G36'),
(12, 'R3', 'P03', 'Hipertensi dalam Kehamilan (Eklampsia)', 'G06'),
(13, 'R3', 'P03', 'Hipertensi dalam Kehamilan (Eklampsia)', 'G26'),
(14, 'R3', 'P03', 'Hipertensi dalam Kehamilan (Eklampsia)', 'G29'),
(15, 'R3', 'P03', 'Hipertensi dalam Kehamilan (Eklampsia)', 'G07'),
(16, 'R4', 'P04', 'Hipertensi dalam Kehamilan (Gestasional)', 'G26'),
(17, 'R4', 'P04', 'Hipertensi dalam Kehamilan (Gestasional)', 'G30'),
(18, 'R4', 'P04', 'Hipertensi dalam Kehamilan (Gestasional)', 'G05'),
(19, 'R4', 'P04', 'Hipertensi dalam Kehamilan (Gestasional)', 'G04'),
(20, 'R5', 'P05', 'Hipertensi dalam Kehamilan (Kronis)', 'G26'),
(21, 'R5', 'P05', 'Hipertensi dalam Kehamilan (Kronis)', 'G07'),
(22, 'R5', 'P05', 'Hipertensi dalam Kehamilan (Kronis)', 'G01'),
(23, 'R6', 'P06', 'Pendarahan (Abortus (Keguguran))', 'G08'),
(24, 'R6', 'P06', 'Pendarahan (Abortus (Keguguran))', 'G10'),
(25, 'R6', 'P06', 'Pendarahan (Abortus (Keguguran))', 'G11'),
(26, 'R6', 'P06', 'Pendarahan (Abortus (Keguguran))', 'G32'),
(27, 'R6', 'P06', 'Pendarahan (Abortus (Keguguran))', 'G33'),
(28, 'R7', 'P07', 'Pendarahan (Plasenta Previa)', 'G10'),
(29, 'R7', 'P07', 'Pendarahan (Plasenta Previa)', 'G35'),
(30, 'R7', 'P07', 'Pendarahan (Plasenta Previa)', 'G14'),
(31, 'R7', 'P07', 'Pendarahan (Plasenta Previa)', 'G42'),
(32, 'R7', 'P07', 'Pendarahan (Plasenta Previa)', 'G36'),
(33, 'R8', 'P08', 'Pendarahan (Solusio Plasenta)', 'G10'),
(34, 'R8', 'P08', 'Pendarahan (Solusio Plasenta)', 'G09'),
(35, 'R8', 'P08', 'Pendarahan (Solusio Plasenta)', 'G24'),
(36, 'R8', 'P08', 'Pendarahan (Solusio Plasenta)', 'G14'),
(37, 'R8', 'P08', 'Pendarahan (Solusio Plasenta)', 'G36'),
(38, 'R8', 'P08', 'Pendarahan (Solusio Plasenta)', 'G42'),
(39, 'R9', 'P09', 'Pendarahan (Subinvolusi Uteri)', 'G10'),
(40, 'R9', 'P09', 'Pendarahan (Subinvolusi Uteri)', 'G13'),
(41, 'R9', 'P09', 'Pendarahan (Subinvolusi Uteri)', 'G34'),
(42, 'R9', 'P09', 'Pendarahan (Subinvolusi Uteri)', 'G38'),
(43, 'R9', 'P09', 'Pendarahan (Subinvolusi Uteri)', 'G22'),
(44, 'R9', 'P09', 'Pendarahan (Subinvolusi Uteri)', 'G27'),
(45, 'R10', 'P10', 'Infeksi dan Penyakit Penyerta (Demam Unspecified)', 'G15'),
(46, 'R10', 'P10', 'Infeksi dan Penyakit Penyerta (Demam Unspecified)', 'G38'),
(47, 'R10', 'P10', 'Infeksi dan Penyakit Penyerta (Demam Unspecified)', 'G23'),
(48, 'R10', 'P10', 'Infeksi dan Penyakit Penyerta (Demam Unspecified)', 'G09'),
(49, 'R11', 'P11', 'Infeksi dan Penyakit Penyerta (Triple E/Eliminasi)', 'G39'),
(50, 'R11', 'P11', 'Infeksi dan Penyakit Penyerta (Triple E/Eliminasi)', 'G25'),
(51, 'R11', 'P11', 'Infeksi dan Penyakit Penyerta (Triple E/Eliminasi)', 'G16'),
(52, 'R11', 'P11', 'Infeksi dan Penyakit Penyerta (Triple E/Eliminasi)', 'G18'),
(53, 'R12', 'P12', 'Infeksi dan Penyakit Penyerta (Leukorea (Keputihan))', 'G19'),
(54, 'R12', 'P12', 'Infeksi dan Penyakit Penyerta (Leukorea (Keputihan))', 'G13'),
(55, 'R13', 'P13', 'Infeksi dan Penyakit Penyerta (Thypoid (Demam Tifoid))', 'G38'),
(56, 'R13', 'P13', 'Infeksi dan Penyakit Penyerta (Thypoid (Demam Tifoid))', 'G41'),
(57, 'R13', 'P13', 'Infeksi dan Penyakit Penyerta (Thypoid (Demam Tifoid))', 'G20'),
(58, 'R13', 'P13', 'Infeksi dan Penyakit Penyerta (Thypoid (Demam Tifoid))', 'G21'),
(59, 'R13', 'P13', 'Infeksi dan Penyakit Penyerta (Thypoid (Demam Tifoid))', 'G14'),
(60, 'R14', 'P14', 'Infeksi dan Penyakit Penyerta (Demam Berdarah (DBD))', 'G38'),
(61, 'R14', 'P14', 'Infeksi dan Penyakit Penyerta (Demam Berdarah (DBD))', 'G40'),
(62, 'R14', 'P14', 'Infeksi dan Penyakit Penyerta (Demam Berdarah (DBD))', 'G17'),
(63, 'R14', 'P14', 'Infeksi dan Penyakit Penyerta (Demam Berdarah (DBD))', 'G14'),
(64, 'R14', 'P14', 'Infeksi dan Penyakit Penyerta (Demam Berdarah (DBD))', 'G36'),
(65, 'R15', 'P15', 'Infeksi dan Penyakit Penyerta (Ketuban Pecah Dini)', 'G12'),
(66, 'R15', 'P15', 'Infeksi dan Penyakit Penyerta (Ketuban Pecah Dini)', 'G37'),
(67, 'R15', 'P15', 'Infeksi dan Penyakit Penyerta (Ketuban Pecah Dini)', 'G13'),
(68, 'R15', 'P15', 'Infeksi dan Penyakit Penyerta (Ketuban Pecah Dini)', 'G14'),
(69, 'R15', 'P15', 'Infeksi dan Penyakit Penyerta (Ketuban Pecah Dini)', 'G36'),
(70, 'R16', 'P16', 'Anemia (Kehamilan & Nifas)', 'G42'),
(71, 'R16', 'P16', 'Anemia (Kehamilan & Nifas)', 'G22'),
(72, 'R16', 'P16', 'Anemia (Kehamilan & Nifas)', 'G23'),
(73, 'R16', 'P16', 'Anemia (Kehamilan & Nifas)', 'G03'),
(74, 'R16', 'P16', 'Anemia (Kehamilan & Nifas)', 'G14'),
(75, 'R17', 'P17', 'KEK (Kehamilan & Nifas)', 'G43'),
(76, 'R17', 'P17', 'KEK (Kehamilan & Nifas)', 'G23'),
(77, 'R17', 'P17', 'KEK (Kehamilan & Nifas)', 'G14'),
(78, 'R17', 'P17', 'KEK (Kehamilan & Nifas)', 'G36'),
(79, 'R18', 'P18', 'Diabetes Mellitus (DM) Tipe 2 & Gestasional', 'G44'),
(80, 'R18', 'P18', 'Diabetes Mellitus (DM) Tipe 2 & Gestasional', 'G45'),
(81, 'R18', 'P18', 'Diabetes Mellitus (DM) Tipe 2 & Gestasional', 'G34'),
(82, 'R18', 'P18', 'Diabetes Mellitus (DM) Tipe 2 & Gestasional', 'G23');

-- --------------------------------------------------------

--
-- Table structure for table `tb_gejala`
--

CREATE TABLE `tb_gejala` (
  `kode_gejala` varchar(10) NOT NULL,
  `nama_gejala` varchar(255) NOT NULL,
  `pertanyaan_user` text DEFAULT NULL,
  `kategori` enum('Anamnesis','Klinis') DEFAULT 'Anamnesis'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_gejala`
--

INSERT INTO `tb_gejala` (`kode_gejala`, `nama_gejala`, `pertanyaan_user`, `kategori`) VALUES
('G01', 'Sakit kepala hebat atau pusing yang menetap', 'Mengalami sakit kepala hebat atau pusing yang menetap (G01)', 'Anamnesis'),
('G02', 'Nyeri ulu hati (Epigastric pain)', 'Merasakan nyeri pada ulu hati (G02)', 'Anamnesis'),
('G03', 'Pandangan mata kabur / berkunang-kunang', 'Pandangan mata terasa kabur atau berkunang-kunang (G03)', 'Anamnesis'),
('G04', 'Bengkak (Edema) pada wajah atau tangan', 'Mengalami bengkak (edema) pada wajah atau tangan (G04)', 'Klinis'),
('G05', 'Rasa pegal/tegang pada tengkuk', 'Merasakan pegal atau tegang pada tengkuk (G05)', 'Anamnesis'),
('G06', 'Kejang kaku seluruh tubuh atau penurunan kesadaran', 'Mengalami kejang kaku seluruh tubuh atau penurunan kesadaran (G06)', 'Klinis'),
('G07', 'Riwayat Hipertensi sudah ada sebelum hamil (< 20 Minggu)', 'Memiliki riwayat darah tinggi sebelum hamil atau sebelum usia 20 minggu (G07)', 'Anamnesis'),
('G08', 'Keluar darah dari jalan lahir (flek/darah segar)', 'Keluar darah flek atau darah segar dari jalan lahir (G08)', 'Klinis'),
('G09', 'Nyeri perut yang terus-menerus (perut terasa tegang/keras)', 'Merasakan nyeri perut terus-menerus atau perut terasa tegang/keras (G09)', 'Anamnesis'),
('G10', 'Keluar darah dari jalan lahir (Flek / Darah Segar / Gumpalan)', 'Keluar darah berupa flek, darah segar, atau gumpalan dari jalan lahir (G10)', 'Klinis'),
('G11', 'Keluar jaringan (seperti daging/selaput) dari jalan lahir', 'Keluar jaringan seperti daging atau selaput dari jalan lahir (G11)', 'Klinis'),
('G12', 'Keluar air merembes (ketuban) dari jalan lahir', 'Keluar air merembes atau air ketuban dari jalan lahir (G12)', 'Klinis'),
('G13', 'Cairan vagina/nifas berbau busuk, bernanah, atau berbusa', 'Cairan vagina atau nifas berbau busuk, bernanah, atau berbusa (G13)', 'Klinis'),
('G14', 'Gerak janin terasa berkurang (< 10x dalam 12 jam)', 'Gerakan janin terasa berkurang atau kurang dari 10 kali dalam 12 jam (G14)', 'Anamnesis'),
('G15', 'Demam tinggi atau menggigil', 'Mengalami demam tinggi atau menggigil (G15)', 'Klinis'),
('G16', 'Mata atau kulit tampak kuning (Ikterus)', 'Mata atau kulit tampak berwarna kuning (G16)', 'Klinis'),
('G17', 'Muncul bintik merah di kulit / Mimisan / Gusi berdarah', 'Muncul bintik merah di kulit, mimisan, atau gusi berdarah (G17)', 'Klinis'),
('G18', 'Luka lecet / koreng pada area kemaluan', 'Terdapat luka lecet atau koreng pada area kemaluan (G18)', 'Klinis'),
('G19', 'Gatal, panas, atau perih di area kemaluan', 'Merasakan gatal, panas, atau perih di area kemaluan (G19)', 'Anamnesis'),
('G20', 'Gangguan BAB (Diare/Sembelit) atau Mual Muntah', 'Mengalami gangguan BAB atau mual muntah (G20)', 'Anamnesis'),
('G21', 'Lidah kotor (putih di tengah dengan tepi merah)', 'Lidah tampak kotor, putih di tengah dengan tepi merah (G21)', 'Klinis'),
('G22', 'Wajah, kelopak mata dalam, atau telapak tangan tampak pucat', 'Wajah, kelopak mata dalam, atau telapak tangan tampak pucat (G22)', 'Klinis'),
('G23', 'Badan terasa Lemah, Letih, Lesu (5L) / Mudah lelah', 'Badan terasa lemah, letih, lesu, atau mudah lelah (G23)', 'Anamnesis'),
('G24', 'Riwayat jatuh / trauma benturan pada perut', 'Memiliki riwayat jatuh atau trauma benturan pada perut (G24)', 'Anamnesis'),
('G25', 'Riwayat kontak seksual berisiko (Gonta-ganti pasangan)', 'Memiliki riwayat kontak seksual berisiko atau gonta-ganti pasangan (G25)', 'Anamnesis'),
('G26', 'Tekanan Darah Tinggi (≥140/90 mmHg)', 'Hasil tekanan darah tinggi ≥140/90 mmHg (G26)', 'Klinis'),
('G27', 'Tekanan Darah Rendah / Hipotensi (≤90/60 mmHg)', 'Hasil tekanan darah rendah ≤90/60 mmHg (G27)', 'Klinis'),
('G28', 'Protein Urine Positif 1 (+1)', 'Hasil lab Protein Urine Positif 1 (G28)', 'Klinis'),
('G29', 'Protein Urine Positif 2 (≥+2)', 'Hasil lab Protein Urine Positif 2 atau lebih (G29)', 'Klinis'),
('G30', 'Protein Urine Negatif (-)', 'Hasil lab Protein Urine Negatif (G30)', 'Klinis'),
('G31', 'Respon ketukan lutut berlebihan (Refleks Patella Meningkat)', 'Respon ketukan lutut atau Refleks Patella meningkat (G31)', 'Klinis'),
('G32', 'Tes Kehamilan (PP Test) Positif (+) pada kasus perdarahan', 'Hasil Tes Kehamilan (PP Test) tetap Positif saat terjadi perdarahan (G32)', 'Klinis'),
('G33', 'Pemeriksaan dalam: (Ostium Uteri) Mulut rahim teraba terbuka', 'Hasil pemeriksaan dalam menunjukkan mulut rahim teraba terbuka (G33)', 'Klinis'),
('G34', 'Ukuran perut/rahim tidak sesuai dengan usia kehamilan (Terlalu kecil/besar)', 'Ukuran perut atau rahim tidak sesuai dengan usia kehamilan (G34)', 'Klinis'),
('G35', 'Plasenta menutupi jalan lahir (Hasil USG)', 'Hasil USG menunjukkan plasenta menutupi jalan lahir (G35)', 'Klinis'),
('G36', 'Detak jantung bayi tidak normal (< 120 atau > 180 kali/menit)', 'Detak jantung bayi tidak normal, <120 atau >180 kali/menit (G36)', 'Klinis'),
('G37', 'Cek Kertas Lakmus berubah merah jadi biru (Tanda air ketuban pecah)', 'Kertas Lakmus berubah dari merah menjadi biru saat cek cairan (G37)', 'Klinis'),
('G38', 'Suhu tubuh demam (38°C atau lebih)', 'Suhu tubuh demam mencapai 38°C atau lebih (G38)', 'Klinis'),
('G39', 'Hasil Lab Positif/Reaktif untuk HIV, Sifilis, atau Hepatitis B', 'Hasil Lab Positif atau Reaktif untuk HIV, Sifilis, atau Hepatitis B (G39)', 'Klinis'),
('G40', 'Trombosit Rendah (< 100.000) / Uji Tourniquet Positif', 'Hasil Trombosit rendah atau uji Tourniquet positif (G40)', 'Klinis'),
('G41', 'Hasil Lab Widal / Tubex Positif', 'Hasil Lab Widal atau Tubex Positif (G41)', 'Klinis'),
('G42', 'Kadar Hemoglobin (Hb) Rendah (< 11 gr/dL)', 'Kadar Hemoglobin (Hb) rendah < 11 gr/dL (G42)', 'Klinis'),
('G43', 'Lingkar Lengan Atas (LILA) Kecil (< 23,5 cm) / IMT < 18,5', 'Ukuran LILA kecil < 23,5 cm atau IMT < 18,5 (G43)', 'Klinis'),
('G44', 'Kadar Gula Darah Tinggi / Hiperglikemia (GDS/GDP Tinggi)', 'Kadar gula darah tinggi atau Hiperglikemia (G44)', 'Klinis'),
('G45', 'Sering haus, sering lapar, dan sering buang air kecil', 'Sering merasa haus, sering lapar, dan sering buang air kecil (G45)', 'Anamnesis');

-- --------------------------------------------------------

--
-- Table structure for table `tb_penyakit`
--

CREATE TABLE `tb_penyakit` (
  `kode_penyakit` varchar(10) NOT NULL,
  `nama_penyakit` varchar(100) NOT NULL,
  `definisi` text DEFAULT NULL,
  `solusi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_penyakit`
--

INSERT INTO `tb_penyakit` (`kode_penyakit`, `nama_penyakit`, `definisi`, `solusi`) VALUES
('P01', 'Hipertensi Dalam Kehamilan (Preeklamsia Ringan)', 'Komplikasi kehamilan yang ditandai dengan tekanan darah tinggi (≥140/90 mmHg) dan adanya protein dalam urine setelah usia kehamilan 20 minggu, tanpa tanda-tanda berat.', 'Konsultasi ke Dokter Spesialis Kandungan, kontrol tekanan darah secara rutin, minum obat teratur, serta jaga pola makan dan istirahat.'),
('P02', 'Hipertensi Dalam Kehamilan (Preeklamsia Berat)', 'Kondisi lanjutan dari preeklamsia dengan tekanan darah sangat tinggi (≥160/110 mmHg) disertai gangguan fungsi organ (ginjal/hati) yang membahayakan ibu dan janin.', 'Segera rujuk ke RSUD (PONEK). Membutuhkan pengawasan ketat dan penanganan medis darurat untuk mencegah komplikasi fatal.'),
('P03', 'Hipertensi Dalam Kehamilan (Eklampsia)', 'Kondisi gawat darurat medis yang ditandai dengan terjadinya kejang atau koma pada ibu hamil dengan preeklamsia.', 'Segera rujuk ke RSUD (PONEK). Merupakan kondisi darurat medis (kejang) yang mengancam nyawa ibu dan janin.'),
('P04', 'Hipertensi Dalam Kehamilan (Gestasional)', 'Tekanan darah tinggi yang muncul setelah usia kehamilan 20 minggu tanpa adanya protein dalam urine dan menghilang setelah melahirkan.', 'Konsultasi ke Dokter Spesialis Kandungan, pemantauan tensi berkala, menjaga pola hidup sehat (makan & istirahat), dan konsumsi obat sesuai anjuran.'),
('P05', 'Hipertensi Dalam Kehamilan (Kronis)', 'Tekanan darah tinggi yang sudah ada sebelum kehamilan, didiagnosis sebelum usia kehamilan 20 minggu, atau berlanjut hingga 12 minggu pasca persalinan.', 'Konsultasi ke Dokter Spesialis Kandungan, kontrol rutin untuk mencegah kenaikan tensi ekstrem, minum obat teratur, dan diet rendah garam/sehat.'),
('P06', 'Perdarahan (Abortus (Keguguran))', 'Berakhirnya kehamilan sebelum janin dapat hidup di luar kandungan (usia kehamilan < 20 minggu) atau berat janin < 500 gram.', 'Stabilisasi cairan (infus), pemberian obat penguat atau penghenti darah, dan tindakan medis Kuretase untuk pembersihan sisa jaringan.'),
('P07', 'Perdarahan (Plasenta Previa)', 'Kondisi di mana plasenta (ari-ari) menutupi sebagian atau seluruh jalan lahir (mulut rahim), menyebabkan risiko perdarahan hebat.', 'Stabilisasi cairan (infus) ketat dan tindakan medis bedah Sectio Caesarea (SC) karena jalan lahir tertutup plasenta.'),
('P08', 'Perdarahan (Solusio Plasenta)', 'Terlepasnya plasenta dari dinding rahim bagian dalam sebelum proses persalinan terjadi, yang dapat memutus suplai oksigen ke bayi.', 'Stabilisasi cairan (infus) cepat dan tindakan medis darurat Sectio Caesarea (SC) untuk menyelamatkan nyawa ibu dan janin.'),
('P09', 'Perdarahan (Subinvolusi Uteri)', 'Kegagalan rahim untuk kembali ke ukuran normal setelah persalinan, yang menyebabkan perdarahan berkepanjangan pada masa nifas.', 'Stabilisasi cairan (infus), pemberian obat kontraksi rahim (uterotonika), serta tindakan Masase (pijat) uterus untuk menghentikan perdarahan.'),
('P10', 'Infeksi Dan Penyakit Penyerta (Demam Unspecified)', 'Peningkatan suhu tubuh ibu hamil/nifas di atas batas normal tanpa penyebab spesifik yang belum teridentifikasi secara klinis.', 'Jika demam tinggi berlanjut lebih dari 3 hari, segera lakukan pemeriksaan laboratorium untuk mendeteksi risiko Tifoid atau DBD.'),
('P11', 'Infeksi Dan Penyakit Penyerta (Triple E/ Eliminasi)', 'Upaya deteksi dini penularan infeksi HIV, Sifilis, dan Hepatitis B dari ibu ke anak yang berisiko cacat atau kematian janin.', 'Wajib melakukan Tes Laboratorium Triple Eliminasi (Skrining HIV, Sifilis, dan Hepatitis B) untuk mencegah penularan ke janin/bayi.'),
('P12', 'Infeksi Dan Penyakit Penyerta (Leukorea (Keputihan))', 'Keluarnya cairan berlebihan dari vagina yang bisa bersifat fisiologis atau patologis (akibat infeksi jamur/bakteri) yang berisiko bagi kehamilan.', 'Menjaga kebersihan area kewanitaan (Personal Hygiene) secara ketat dan pemberian Terapi Antibiotik sesuai resep dokter jika terindikasi infeksi.'),
('P13', 'Infeksi Dan Penyakit Penyerta (Thypoid (Demam Tifoid))', 'Infeksi bakteri Salmonella typhi yang menyebar melalui makanan, menyebabkan demam tinggi berkepanjangan dan gangguan pencernaan.', 'Pemberian Terapi Antibiotik, observasi ketat, serta pemeriksaan lab darah secara berkala untuk memantau perkembangan bakteri.'),
('P14', 'Infeksi Dan Penyakit Penyerta (Demam Berdarah/DBD)', 'Infeksi virus Dengue yang ditularkan nyamuk Aedes aegypti, berisiko menyebabkan penurunan trombosit drastis dan perdarahan.', 'Pemeriksaan lab (Cek Trombosit & Hemoglobin), pemantauan cairan tubuh (infus jika perlu), dan istirahat total.'),
('P15', 'Infeksi Dan Penyakit Penyerta (KPD/ Ketuban Pecah Dini)', 'Pecahnya selaput ketuban sebelum adanya tanda-tanda persalinan (inpartu), meningkatkan risiko infeksi pada ibu dan bayi.', 'Segera ke RS. Diperlukan pemeriksaan lab lengkap (Darah & Urine) serta pemberian Antibiotik untuk mencegah infeksi pada ibu dan janin.'),
('P16', 'Anemia (Kehamilan & Nifas)', 'Kondisi medis dimana kadar Hemoglobin (Hb) dalam darah lebih rendah dari normal (< 11 g/dL pada ibu hamil), mengurangi suplai oksigen ke janin.', 'Minum minimal 90 Tablet Tambah Darah (TTD) selama kehamilan. Lakukan cek kadar Hb (Hemoglobin) ulang pada Trimester 3 dan setelah melahirkan (pasca salin) untuk memastikan kecukupan sel darah merah.'),
('P17', 'KEK/Kurang Energi Kronis (Kehamilan & Nifas)', 'Kondisi kekurangan gizi yang berlangsung lama (menahun) ditandai dengan ukuran Lingkar Lengan Atas (LILA) < 23,5 cm.', 'Tingkatkan asupan protein hewani & nabati secara signifikan. Pantau ukuran LILA (Lingkar Lengan Atas) secara berkala untuk memastikan kenaikan berat badan dan status gizi membaik.'),
('P18', 'Diabetes Mellitus (DM) Tipe 2 Dan Gestasional', 'Gangguan toleransi glukosa atau kadar gula darah tinggi yang terjadi atau pertama kali ditemukan saat masa kehamilan.', 'Manajemen Gula Darah. Diet rendah gula sesuai arahan ahli gizi, olahraga ringan, dan kontrol rutin ke Dokter Sp.OG/Penyakit Dalam. Pantau gerak janin secara mandiri setiap hari.');

-- --------------------------------------------------------

--
-- Table structure for table `tb_riwayat`
--

CREATE TABLE `tb_riwayat` (
  `id_riwayat` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `kode_penyakit` varchar(10) DEFAULT NULL,
  `tanggal_konsultasi` timestamp NOT NULL DEFAULT current_timestamp(),
  `hasil_diagnosa` text DEFAULT NULL,
  `gejala_terpilih` text DEFAULT NULL,
  `saran_penanganan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_riwayat`
--

INSERT INTO `tb_riwayat` (`id_riwayat`, `id_user`, `kode_penyakit`, `tanggal_konsultasi`, `hasil_diagnosa`, `gejala_terpilih`, `saran_penanganan`) VALUES
(1, 1, NULL, '2026-02-01 02:47:14', 'P01 - Preeklamsia (Hipertensi dalam Kehamilan) (Tipe Berat (Gejala Lengkap))', 'G03, G04, G05, G06, G01, G02', 'Kondisi ini memerlukan pemantauan ketat demi keselamatan ibu dan janin. Segera kunjungi RSUD (Layanan PONEK) untuk mendapatkan perawatan stabilisasi tekanan darah. Sementara itu, ibu sangat dianjurkan untuk beristirahat total (bed rest) dengan posisi miring ke kiri agar aliran darah ke bayi tetap lancar.'),
(2, 1, NULL, '2026-02-01 02:58:54', 'P01 - Preeklamsia (Hipertensi dalam Kehamilan) (Tipe Berat (Gejala Lengkap))', 'G03, G04, G05, G06, G01, G02', 'Kondisi ini memerlukan pemantauan ketat demi keselamatan ibu dan janin. Segera kunjungi RSUD (Layanan PONEK) untuk mendapatkan perawatan stabilisasi tekanan darah. Sementara itu, ibu sangat dianjurkan untuk beristirahat total (bed rest) dengan posisi miring ke kiri agar aliran darah ke bayi tetap lancar.'),
(3, 1, NULL, '2026-02-01 03:07:51', 'Indikasi Gejala (Observasi)', 'G04, G06, G18', '\n                    1. Istirahat yang cukup dan kurangi aktivitas berat.\n                    2. Pantau terus jika muncul gejala baru dalam 24 jam.\n                    3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.\n                    '),
(4, 7, NULL, '2026-02-01 04:59:28', 'P03 - Infeksi Maternal (Sepsis Nifas Berat)', 'G03, G04, G17, G18, G12, G14, G15', 'Lakukan pemeriksaan ke fasilitas kesehatan untuk mendapatkan terapi pengobatan yang tepat guna mengatasi penyebab infeksi. Ibu disarankan untuk meningkatkan kebersihan diri (personal hygiene) dan memastikan asupan cairan yang cukup, serta memantau suhu tubuh secara rutin di rumah.'),
(5, 7, NULL, '2026-02-01 05:02:45', 'Indikasi Gejala (Observasi)', 'G04, G06', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(6, 7, NULL, '2026-02-02 01:25:24', 'Indikasi Gejala (Observasi)', 'G04, G06, G08', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(7, 7, NULL, '2026-02-02 06:11:22', 'Indikasi Gejala (Observasi)', 'G04, G06', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(8, 7, 'P02', '2026-02-02 06:13:57', 'Perdarahan (Hemorrhage) (Pendarahan Berulang (Anemia Berat))', 'G04, G08, G09, G17, G18, G16', 'Prioritas Keselamatan Utama. Segera bawa ibu ke IGD Rumah Sakit terdekat untuk mendapatkan pertolongan medis segera. Petugas kesehatan akan melakukan tindakan stabilisasi cairan tubuh (rehidrasi) untuk menjaga kondisi ibu tetap aman. Pastikan ada pendamping dari keluarga yang siaga untuk dukungan donor darah.'),
(9, 12, NULL, '2026-02-02 20:08:40', 'Indikasi Gejala (Observasi)', 'G04, G06, G08', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(10, 12, 'P01', '2026-02-02 23:19:07', 'Preeklamsia (Hipertensi dalam Kehamilan) (Tipe Berat disertai Distres Janin)', 'G03, G06, G18, G19, G01, G02', 'Kondisi ini memerlukan pemantauan ketat demi keselamatan ibu dan janin. Segera kunjungi RSUD (Layanan PONEK) untuk mendapatkan perawatan stabilisasi tekanan darah. Sementara itu, ibu sangat dianjurkan untuk beristirahat total (bed rest) dengan posisi miring ke kiri agar aliran darah ke bayi tetap lancar.'),
(11, 13, NULL, '2026-02-03 01:07:03', 'Indikasi Gejala (Observasi)', 'G04, G06, G08', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(12, 14, 'P01', '2026-02-03 02:28:24', 'Preeklamsia (Hipertensi dalam Kehamilan) (Tipe Berat disertai Distres Janin)', 'G03, G06, G18, G19, G01, G02', 'Kondisi ini memerlukan pemantauan ketat demi keselamatan ibu dan janin. Segera kunjungi RSUD (Layanan PONEK) untuk mendapatkan perawatan stabilisasi tekanan darah. Sementara itu, ibu sangat dianjurkan untuk beristirahat total (bed rest) dengan posisi miring ke kiri agar aliran darah ke bayi tetap lancar.'),
(13, 14, NULL, '2026-02-03 02:29:30', 'Indikasi Gejala (Observasi)', 'G04, G06, G07, G11', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(14, 14, 'P01', '2026-02-03 04:01:10', 'Preeklamsia (Hipertensi dalam Kehamilan) (Tipe Berat disertai Distres Janin)', 'G03, G06, G18, G19, G01, G02', 'Kondisi ini memerlukan pemantauan ketat demi keselamatan ibu dan janin. Segera kunjungi RSUD (Layanan PONEK) untuk mendapatkan perawatan stabilisasi tekanan darah. Sementara itu, ibu sangat dianjurkan untuk beristirahat total (bed rest) dengan posisi miring ke kiri agar aliran darah ke bayi tetap lancar.'),
(15, 14, 'P01', '2026-02-03 04:26:57', 'Preeklamsia (Hipertensi dalam Kehamilan) (Tipe Berat disertai Distres Janin)', 'G03, G06, G18, G19, G01, G02', 'Kondisi ini memerlukan pemantauan ketat demi keselamatan ibu dan janin. Segera kunjungi RSUD (Layanan PONEK) untuk mendapatkan perawatan stabilisasi tekanan darah. Sementara itu, ibu sangat dianjurkan untuk beristirahat total (bed rest) dengan posisi miring ke kiri agar aliran darah ke bayi tetap lancar.'),
(16, 14, NULL, '2026-02-03 04:42:58', 'Indikasi Gejala (Observasi)', 'G04, G06, G08, G13', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(17, 16, 'P01', '2026-02-03 19:50:09', 'Preeklamsia (Hipertensi dalam Kehamilan) (Tipe Berat disertai Distres Janin)', 'G03, G06, G18, G19, G01, G02', 'Kondisi ini memerlukan pemantauan ketat demi keselamatan ibu dan janin. Segera kunjungi RSUD (Layanan PONEK) untuk mendapatkan perawatan stabilisasi tekanan darah. Sementara itu, ibu sangat dianjurkan untuk beristirahat total (bed rest) dengan posisi miring ke kiri agar aliran darah ke bayi tetap lancar.'),
(18, 14, 'P02', '2026-02-05 05:26:47', 'Perdarahan (Hemorrhage) (Postpartum Atonia Uteri)', 'G08, G17, G18, G11, G12, G16', 'Prioritas Keselamatan Utama. Segera bawa ibu ke IGD Rumah Sakit terdekat untuk mendapatkan pertolongan medis segera. Petugas kesehatan akan melakukan tindakan stabilisasi cairan tubuh (rehidrasi) untuk menjaga kondisi ibu tetap aman. Pastikan ada pendamping dari keluarga yang siaga untuk dukungan donor darah.'),
(19, 14, NULL, '2026-02-05 05:31:59', 'Indikasi Gejala (Observasi)', 'G04, G06, G18', '1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik.'),
(20, 18, 'P02', '2026-02-05 18:22:39', 'Perdarahan (Hemorrhage) (Postpartum Atonia Uteri)', 'G08, G17, G18, G11, G12, G16', 'Prioritas Keselamatan Utama. Segera bawa ibu ke IGD Rumah Sakit terdekat untuk mendapatkan pertolongan medis segera. Petugas kesehatan akan melakukan tindakan stabilisasi cairan tubuh (rehidrasi) untuk menjaga kondisi ibu tetap aman. Pastikan ada pendamping dari keluarga yang siaga untuk dukungan donor darah.'),
(21, 18, 'P02', '2026-02-06 03:31:41', 'Perdarahan (Hemorrhage) (Postpartum Atonia Uteri)', 'G08, G17, G18, G11, G12, G16', 'Prioritas Keselamatan Utama. Segera bawa ibu ke IGD Rumah Sakit terdekat untuk mendapatkan pertolongan medis segera. Petugas kesehatan akan melakukan tindakan stabilisasi cairan tubuh (rehidrasi) untuk menjaga kondisi ibu tetap aman. Pastikan ada pendamping dari keluarga yang siaga untuk dukungan donor darah.'),
(22, 14, 'P01', '2026-02-12 08:46:01', 'Hipertensi Dalam Kehamilan (Preeklamsia Ringan) (Hipertensi dalam Kehamilan (Preeklamsia Ringan))', 'G04, G26, G28', 'Konsultasi ke Dokter Spesialis Kandungan, kontrol tekanan darah secara rutin, minum obat teratur, serta jaga pola makan dan istirahat.');

-- --------------------------------------------------------

--
-- Table structure for table `tb_user`
--

CREATE TABLE `tb_user` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) DEFAULT NULL,
  `usia` int(11) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `hp` varchar(15) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_user`
--

INSERT INTO `tb_user` (`id_user`, `username`, `password`, `nama_lengkap`, `usia`, `alamat`, `hp`, `created_at`) VALUES
(1, 'bunda', '12345', 'Bunda Tester', 28, 'Jl. Mawar No 10', '08123456789', '2026-01-31 02:55:13'),
(2, 'Raline', '123', 'Raline Shah', 25, 'Jl.Wahidin', '081234557812', '2026-01-31 02:55:13'),
(3, 'raisa', '1234', 'Raisa Andriani', 27, 'Jl.Jagakarsa', '082323462634', '2026-01-31 02:55:13'),
(4, 'lisa', '12345', 'Lisa Andriani', 28, 'Jl.Dr.Sutomo', '082435235212', '2026-01-31 02:55:13'),
(5, 'tes', '12', 'tesaja', 29, 'Jl.Soedirman', '081234532734', '2026-01-31 02:55:13'),
(6, 'apa', '1234567', 'apaya', 26, 'Jl. Malioboro', '088776325233', '2026-01-31 02:55:13'),
(7, 'bunda_renata', '1dan2', 'Renata Moeloek', 26, 'Jl. R.A. Kartini', '081424626411', '2026-02-01 04:55:55'),
(8, 'bunda_raisha', 'mejiku', 'raisha', 22, 'Jl. Veteran', '082354673212', '2026-02-02 13:24:10'),
(10, 'bunda_martha', '1234m', 'Martha', 27, 'Jl. Dewi Sartika', '081243126744', '2026-02-02 17:35:52'),
(11, 'bunda_rifah', '1234r', 'Syarifah', 24, 'Jl. Jenderal Sudirman', '083456774433', '2026-02-02 17:43:57'),
(12, 'bunda_tesuji', 'tesuji123', 'Meriem', 24, 'Jl. Merdekaa', '083312454432', '2026-02-02 19:43:12'),
(13, 'bunda_namira', 'namira123', 'Namira Naya', 27, 'Jl. Mekar Sari', '083321567734', '2026-02-03 01:05:54'),
(14, 'bunda_ranti', 'ranti123', 'Ranti Hanafiah Suriati', 24, 'Jl. Lubuk Begalung', '081122333445', '2026-02-03 02:26:48'),
(16, 'bunda_yolanda', 'yolan123', 'Yolanda Putri', 34, 'Solok Selatan', '08127643224577', '2026-02-03 19:39:47'),
(17, 'bunda_ayu', 'ayu123', 'Ayu Afrianti', 33, 'Solok Selatan', '08233244766811', '2026-02-03 22:43:57'),
(18, 'bunda_ariska', 'ariska123', 'Wira Ariska', 28, 'Sungai Talu', '082234664581', '2026-02-05 13:11:13'),
(19, 'bunda_lova', 'lova123', 'Lova Feranita', 41, 'Solok Selatan', '082344124532', '2026-02-05 19:17:33');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_admin`
--
ALTER TABLE `tb_admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indexes for table `tb_aturan`
--
ALTER TABLE `tb_aturan`
  ADD PRIMARY KEY (`id_aturan`),
  ADD KEY `kode_penyakit` (`kode_penyakit`),
  ADD KEY `kode_gejala` (`kode_gejala`);

--
-- Indexes for table `tb_gejala`
--
ALTER TABLE `tb_gejala`
  ADD PRIMARY KEY (`kode_gejala`);

--
-- Indexes for table `tb_penyakit`
--
ALTER TABLE `tb_penyakit`
  ADD PRIMARY KEY (`kode_penyakit`);

--
-- Indexes for table `tb_riwayat`
--
ALTER TABLE `tb_riwayat`
  ADD PRIMARY KEY (`id_riwayat`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `kode_penyakit` (`kode_penyakit`);

--
-- Indexes for table `tb_user`
--
ALTER TABLE `tb_user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_admin`
--
ALTER TABLE `tb_admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `tb_aturan`
--
ALTER TABLE `tb_aturan`
  MODIFY `id_aturan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT for table `tb_riwayat`
--
ALTER TABLE `tb_riwayat`
  MODIFY `id_riwayat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `tb_user`
--
ALTER TABLE `tb_user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_aturan`
--
ALTER TABLE `tb_aturan`
  ADD CONSTRAINT `tb_aturan_ibfk_1` FOREIGN KEY (`kode_penyakit`) REFERENCES `tb_penyakit` (`kode_penyakit`) ON DELETE CASCADE,
  ADD CONSTRAINT `tb_aturan_ibfk_2` FOREIGN KEY (`kode_gejala`) REFERENCES `tb_gejala` (`kode_gejala`) ON DELETE CASCADE;

--
-- Constraints for table `tb_riwayat`
--
ALTER TABLE `tb_riwayat`
  ADD CONSTRAINT `tb_riwayat_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `tb_user` (`id_user`) ON DELETE CASCADE,
  ADD CONSTRAINT `tb_riwayat_ibfk_2` FOREIGN KEY (`kode_penyakit`) REFERENCES `tb_penyakit` (`kode_penyakit`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
