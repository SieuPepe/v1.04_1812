-- ============================================================================
-- HydroFlow Manager - Creación de tabla dim_concejos
-- Concejos de Álava (entidades locales menores dentro de municipios)
-- ============================================================================

-- Crear tabla dim_concejos
CREATE TABLE IF NOT EXISTS dim_concejos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    municipio_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (municipio_id) REFERENCES dim_municipios(id),
    INDEX idx_municipio (municipio_id),
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT de Concejos por Municipio
-- Datos obtenidos de: https://es.wikipedia.org/wiki/Anexo:Concejos_de_Álava
-- ============================================================================

-- Alegría-Dulantzi (municipio_id = 21)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(21, 'Alegría-Dulantzi'),
(21, 'Egileta');

-- Amurrio (municipio_id = 1)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(1, 'Aloria'),
(1, 'Amurrio'),
(1, 'Artomaña'),
(1, 'Baranbio'),
(1, 'Delika'),
(1, 'Larrinbe'),
(1, 'Lekamaña'),
(1, 'Lezama'),
(1, 'Saratxo'),
(1, 'Tertanga');

-- Añana (municipio_id = 35)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(35, 'Atiega');

-- Aramaio (municipio_id = 29)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(29, 'Oleta');

-- Armiñón (municipio_id = 36)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(36, 'Armiñón'),
(36, 'Estavillo');

-- Arraia-Maeztu (municipio_id = 46)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(46, 'Apellániz/Apinaiz'),
(46, 'Atauri'),
(46, 'Azazeta'),
(46, 'Korres'),
(46, 'Maeztu/Maestu'),
(46, 'Onraita/Erroeta'),
(46, 'Real Valle de Laminoria/Laminoriako Erret Harana'),
(46, 'Róitegui/Erroitegi'),
(46, 'Sabando'),
(46, 'Vírgala Mayor/Birgara Goien');

-- Arratzua-Ubarrundia (municipio_id = 30)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(30, 'Arroiabe'),
(30, 'Arzubiaga'),
(30, 'Betolaza'),
(30, 'Ziriano'),
(30, 'Durana'),
(30, 'Landa'),
(30, 'Luko'),
(30, 'Mendibil'),
(30, 'Ullíbarri-Gamboa'),
(30, 'Zurbano/Zurbao');

-- Asparrena (municipio_id = 22)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(22, 'Albeiz/Albéniz'),
(22, 'Ametzaga Asparrena'),
(22, 'Andoin'),
(22, 'Arriola'),
(22, 'Egino'),
(22, 'Gordoa'),
(22, 'Ibarguren'),
(22, 'Ilarduia'),
(22, 'Urabain');

-- Ayala / Aiara (municipio_id = 3)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(3, 'Agiñaga'),
(3, 'Añes'),
(3, 'Arespalditza/Respaldiza'),
(3, 'Costera/Opellora'),
(3, 'Etxegoien'),
(3, 'Erbi'),
(3, 'Izoria'),
(3, 'Lejarzo/Lexartzu'),
(3, 'Llanteno'),
(3, 'Luxo/Lujo'),
(3, 'Luiaondo'),
(3, 'Madaria'),
(3, 'Maroño'),
(3, 'Menagarai-Beotegi'),
(3, 'Menoio'),
(3, 'Murga'),
(3, 'Olabezar'),
(3, 'Ozeka'),
(3, 'Quejana/Kexaa'),
(3, 'Retes de Llanteno'),
(3, 'Salmantón'),
(3, 'Soxo/Sojo'),
(3, 'Zuaza/Zuhatza');

-- Barrundia (municipio_id = 23)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(23, 'Audikana'),
(23, 'Dallo'),
(23, 'Elgea'),
(23, 'Etura'),
(23, 'Etxabarri Urtupiña'),
(23, 'Gebara'),
(23, 'Heredia'),
(23, 'Hermua'),
(23, 'Larrea'),
(23, 'Marieta-Larrintzar'),
(23, 'Maturana'),
(23, 'Mendixur/Mendíjur'),
(23, 'Ozaeta');

-- Berantevilla (municipio_id = 37)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(37, 'Berantevilla'),
(37, 'Lacervilla'),
(37, 'Mijancas'),
(37, 'Santa Cruz del Fierro'),
(37, 'Santurde'),
(37, 'Tobera');

-- Bernedo (municipio_id = 47)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(47, 'Angostina'),
(47, 'Arluzea'),
(47, 'Bernedo'),
(47, 'Markinez'),
(47, 'Navarrete'),
(47, 'Okina'),
(47, 'Quintana'),
(47, 'San Román de Campezo/Durruma Kanpezu'),
(47, 'Urarte'),
(47, 'Urturi'),
(47, 'Villafría');

-- Campezo / Kanpezu (municipio_id = 48)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(48, 'Antoñana'),
(48, 'Bujanda'),
(48, 'Orbiso'),
(48, 'Oteo'),
(48, 'Santa Cruz de Campezo/Santikurutze Kanpezu');

-- Zigoitia (municipio_id = 33)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(33, 'Acosta/Okoizta'),
(33, 'Apodaka'),
(33, 'Berrikano'),
(33, 'Buruaga'),
(33, 'Zestafe'),
(33, 'Etxaguen'),
(33, 'Etxabarri Ibiña'),
(33, 'Eribe'),
(33, 'Gopegi'),
(33, 'Letona'),
(33, 'Manurga'),
(33, 'Mendarozketa'),
(33, 'Murua'),
(33, 'Olano'),
(33, 'Ondategi'),
(33, 'Zaitegi');

-- Kuartango (municipio_id = 39)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(39, 'Anda'),
(39, 'Aprikano'),
(39, 'Etxabarri Kuartango'),
(39, 'Jokano'),
(39, 'Luna'),
(39, 'Marinda'),
(39, 'Sendadiano'),
(39, 'Uribarri Kuartango'),
(39, 'Urbina Eza'),
(39, 'Zuhatzu Kuartango');

-- Elburgo / Burgelu (municipio_id = 24)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(24, 'Añua'),
(24, 'Arbulu'),
(24, 'Argomaniz'),
(24, 'Elburgo/Burgelu'),
(24, 'Gazeta'),
(24, 'Hijona/Ixona');

-- Iruña de Oca / Iruña Oka (municipio_id = 38)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(38, 'Montevite/Mandaita'),
(38, 'Nanclares de la Oca/Langraiz Oka'),
(38, 'Ollávarre/Olabarri'),
(38, 'Trespuentes'),
(38, 'Víllodas/Billoda');

-- Iruraiz-Gauna (municipio_id = 25)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(25, 'Alaitza'),
(25, 'Arrieta'),
(25, 'Azilu'),
(25, 'Erentxun'),
(25, 'Ezkerekotxa'),
(25, 'Gazeo'),
(25, 'Gauna'),
(25, 'Gereñu'),
(25, 'Jauregi'),
(25, 'Langarika'),
(25, 'Trokoniz');

-- Labastida / Bastida (municipio_id = 10)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(10, 'Salinillas de Buradón/Gatzaga Buradon');

-- Lagrán (municipio_id = 49)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(49, 'Lagran'),
(49, 'Pipaon'),
(49, 'Villaverde');

-- Laguardia (municipio_id = 11)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(11, 'Páganos');

-- Lantarón (municipio_id = 40)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(40, 'Alcedo'),
(40, 'Bergonda/Bergüenda'),
(40, 'Caicedo de Yuso'),
(40, 'Comunión/Komunioi'),
(40, 'Fontecha'),
(40, 'Leciñana del Camino/Leziñana'),
(40, 'Molinilla'),
(40, 'Puentelarrá/Larrazubi'),
(40, 'Salcedo'),
(40, 'Sobrón'),
(40, 'Turiso'),
(40, 'Zubillaga');

-- Oyón-Oion (municipio_id = 17)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(17, 'Barriobusto/Gorrebusto'),
(17, 'Labraza');

-- Peñacerrada-Urizaharra (municipio_id = 51)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(51, 'Baroja-Zumentu'),
(51, 'Faido/Faidu'),
(51, 'Loza'),
(51, 'Montoria'),
(51, 'Payueta/Pagoeta'),
(51, 'Peñacerrada-Urizaharra');

-- Ribera Alta / Erriberagoitia (municipio_id = 41)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(41, 'Antezana de la Ribera'),
(41, 'Anuntzeta/Anúcita'),
(41, 'Arreo'),
(41, 'Artaza-Escota/Artatza-Axkoeta'),
(41, 'Barrón'),
(41, 'Basquiñuelas'),
(41, 'Caicedo-Sopeña'),
(41, 'Hereña'),
(41, 'Lasierra'),
(41, 'Leciñana de la Oca'),
(41, 'Morillas'),
(41, 'Ormijana'),
(41, 'Paúl'),
(41, 'Pobes'),
(41, 'Subijana-Morillas'),
(41, 'Tuyo'),
(41, 'Villabezana'),
(41, 'Villaluenga'),
(41, 'Villambrosa'),
(41, 'Viloria');

-- Ribera Baja / Erriberabeitia (municipio_id = 42)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(42, 'Igay'),
(42, 'Manzanos'),
(42, 'Melledes'),
(42, 'Quintanilla de la Ribera'),
(42, 'Rivabellosa'),
(42, 'Rivaguda');

-- San Millán / Donemiliaga (municipio_id = 27)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(27, 'Adana'),
(27, 'Axpuru'),
(27, 'Bikuña/Vicuña'),
(27, 'Eguílaz/Egilatz'),
(27, 'Galarreta'),
(27, 'Luzuriaga'),
(27, 'Mezkia'),
(27, 'Munain'),
(27, 'Narbaiza'),
(27, 'Okariz'),
(27, 'Ordoñana/Erdoñana'),
(27, 'Durruma/San Román de San Millán'),
(27, 'Txintxetru'),
(27, 'Ullibarri-Jauregi/Uribarri-Jauregi'),
(27, 'Zuazo de San Millán/Zuhatzu Donemiliaga');

-- Urkabustaiz (municipio_id = 32)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(32, 'Abezia'),
(32, 'Abornikano'),
(32, 'Beluntza'),
(32, 'Goiuri-Ondona'),
(32, 'Inoso'),
(32, 'Izarra'),
(32, 'Larrazkueta'),
(32, 'Oiardo'),
(32, 'Untza-Apregindana'),
(32, 'Uzkiano');

-- Valdegovía / Gaubea (municipio_id = 44)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(44, 'Acebedo'),
(44, 'Bachicabo'),
(44, 'Barrio'),
(44, 'Basabe'),
(44, 'Bóveda'),
(44, 'Caranca y Mioma'),
(44, 'Karkamu'),
(44, 'Corro'),
(44, 'Espejo'),
(44, 'Fresneda'),
(44, 'Gurendes-Quejo'),
(44, 'Nograro'),
(44, 'Osma'),
(44, 'Pinedo'),
(44, 'Quintanilla'),
(44, 'Tobillas'),
(44, 'Tuesta'),
(44, 'Valderejo'),
(44, 'Valluerca'),
(44, 'Villamaderne-Bellojín'),
(44, 'Villanañe'),
(44, 'Villanueva de Valdegovía');

-- Valle de Arana / Harana (municipio_id = 52)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(52, 'Alda'),
(52, 'Kontrasta'),
(52, 'San Vicente de Arana/Done Bikendi Harana'),
(52, 'Ullíbarri-Arana/Uribarri Harana');

-- Legutio (municipio_id = 31) - Villarreal de Álava
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(31, 'Elosu'),
(31, 'Goiain'),
(31, 'Legutio'),
(31, 'Urbina'),
(31, 'Urrunaga');

-- Vitoria (municipio_id = 310)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(310, 'Abetxuko'),
(310, 'Aberasturi'),
(310, 'Ehari/Ali'),
(310, 'Amarita'),
(310, 'Andollu'),
(310, 'Antezana/Andetxa'),
(310, 'Arangiz'),
(310, 'Arkauti/Arcaute'),
(310, 'Arkaia'),
(310, 'Aretxabaleta'),
(310, 'Argandoña'),
(310, 'Ariñiz/Aríñez'),
(310, 'Armentia'),
(310, 'Askartza'),
(310, 'Astegieta'),
(310, 'Berrostegieta'),
(310, 'Betoño'),
(310, 'Bolívar'),
(310, 'Castillo/Gaztelu'),
(310, 'Zerio'),
(310, 'Krispiña/Crispijana'),
(310, 'Elorriaga'),
(310, 'Eskibel'),
(310, 'Estarrona'),
(310, 'Foronda'),
(310, 'Gamarra Mayor/Gamarra Nagusia'),
(310, 'Gamarra Menor'),
(310, 'Gamiz'),
(310, 'Gardelegi'),
(310, 'Gobeo'),
(310, 'Gometxa'),
(310, 'Gereña'),
(310, 'Hueto Abajo/Otobarren'),
(310, 'Otogoien/Hueto Arriba'),
(310, 'Ilarratza'),
(310, 'Jungitu'),
(310, 'Lasarte'),
(310, 'Legarda'),
(310, 'Lermanda'),
(310, 'Lopidana'),
(310, 'Lubiano'),
(310, 'Margarita'),
(310, 'Martioda'),
(310, 'Matauko'),
(310, 'Mendiguren'),
(310, 'Mendiola'),
(310, 'Mendoza'),
(310, 'Miñao/Miñano Mayor'),
(310, 'Miñano Menor/Miñano Gutxia'),
(310, 'Monasterioguren'),
(310, 'Oreitia'),
(310, 'Otazu'),
(310, 'Retana'),
(310, 'Subijana de Álava/Subillana-Gasteiz'),
(310, 'Ullíbarri de los Olleros/Uribarri Nagusia'),
(310, 'Ullíbarri-Arrazua'),
(310, 'Ullíbarri-Viña/Uribarri-Dibiña'),
(310, 'Villafranca'),
(310, 'Yurre/Ihurre'),
(310, 'Zuazo de Vitoria/Zuhatzu'),
(310, 'Zumeltzu');

-- Zambrana (municipio_id = 45)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(45, 'Berganzo'),
(45, 'Ocio'),
(45, 'Portilla/Zabalate'),
(45, 'Zambrana');

-- Zuia (municipio_id = 34)
INSERT INTO dim_concejos (municipio_id, nombre) VALUES
(34, 'Ametzaga Zuia'),
(34, 'Aperregi'),
(34, 'Domaikia'),
(34, 'Gillerna'),
(34, 'Jugo'),
(34, 'Lukiano'),
(34, 'Markina'),
(34, 'Murgia'),
(34, 'Sarria'),
(34, 'Bitoriano'),
(34, 'Zarate');

-- ============================================================================
-- Verificación
-- ============================================================================
SELECT
    m.municipio_nombre,
    COUNT(c.id) as num_concejos
FROM dim_concejos c
JOIN dim_municipios m ON c.municipio_id = m.id
GROUP BY m.id, m.municipio_nombre
ORDER BY num_concejos DESC;

-- Total de concejos
SELECT COUNT(*) as total_concejos FROM dim_concejos;
