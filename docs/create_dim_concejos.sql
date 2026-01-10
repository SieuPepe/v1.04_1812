-- ============================================================================
-- HydroFlow Manager - Creación de tabla dim_concejos
-- Concejos de Álava (entidades locales menores dentro de municipios)
-- ============================================================================

-- Crear tabla dim_concejos
CREATE TABLE IF NOT EXISTS dim_concejos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    municipio_id INT NOT NULL,
    concejo_nombre VARCHAR(100) NOT NULL,
    concejo_nombre_oficial VARCHAR(100),
    activo TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (municipio_id) REFERENCES dim_municipios(id),
    INDEX idx_municipio (municipio_id),
    INDEX idx_nombre (concejo_nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT de Concejos por Municipio
-- Datos obtenidos de: https://es.wikipedia.org/wiki/Anexo:Concejos_de_Álava
-- ============================================================================

-- Alegría-Dulantzi (municipio_id = 21)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(21, 'Alegría de Álava', 'Alegría-Dulantzi'),
(21, 'Eguileta', 'Egileta');

-- Amurrio (municipio_id = 1)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(1, 'Aloria', 'Aloria'),
(1, 'Amurrio', 'Amurrio'),
(1, 'Artómaña', 'Artomaña'),
(1, 'Barambio', 'Baranbio'),
(1, 'Délica', 'Delika'),
(1, 'Larrimbe', 'Larrinbe'),
(1, 'Lecamaña', 'Lekamaña'),
(1, 'Lezama', 'Lezama'),
(1, 'Saracho', 'Saratxo'),
(1, 'Tertanga', 'Tertanga');

-- Añana (municipio_id = 35)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(35, 'Atiega', 'Atiega');

-- Aramaio (municipio_id = 29)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(29, 'Olaeta', 'Oleta');

-- Armiñón (municipio_id = 36)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(36, 'Armiñón', 'Armiñón'),
(36, 'Estavillo', 'Estavillo');

-- Arraia-Maeztu (municipio_id = 46)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(46, 'Apellániz', 'Apellániz/Apinaiz'),
(46, 'Atauri', 'Atauri'),
(46, 'Azáceta', 'Azazeta'),
(46, 'Corres', 'Korres'),
(46, 'Maestu', 'Maeztu/Maestu'),
(46, 'Onraita', 'Onraita/Erroeta'),
(46, 'Real Valle de Laminoria', 'Real Valle de Laminoria/Laminoriako Erret Harana'),
(46, 'Róitegui', 'Róitegui/Erroitegi'),
(46, 'Sabando', 'Sabando'),
(46, 'Vírgala Mayor', 'Vírgala Mayor/Birgara Goien');

-- Arratzua-Ubarrundia (municipio_id = 30)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(30, 'Arroyabe', 'Arroiabe'),
(30, 'Arzubiaga', 'Arzubiaga'),
(30, 'Betolaza', 'Betolaza'),
(30, 'Ciriano', 'Ziriano'),
(30, 'Durana', 'Durana'),
(30, 'Landa', 'Landa'),
(30, 'Luco', 'Luko'),
(30, 'Mendívil', 'Mendibil'),
(30, 'Ullívarri-Gamboa', 'Ullíbarri-Gamboa'),
(30, 'Zurbano', 'Zurbano/Zurbao');

-- Asparrena (municipio_id = 22)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(22, 'Albéniz', 'Albeiz/Albéniz'),
(22, 'Amézaga de Aspárrena', 'Ametzaga Asparrena'),
(22, 'Andóin', 'Andoin'),
(22, 'Arriola', 'Arriola'),
(22, 'Eguino', 'Egino'),
(22, 'Gordoa', 'Gordoa'),
(22, 'Ibarguren', 'Ibarguren'),
(22, 'Ilarduya', 'Ilarduia'),
(22, 'Urabáin', 'Urabain');

-- Ayala / Aiara (municipio_id = 3)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(3, 'Aguíñiga', 'Agiñaga'),
(3, 'Añes', 'Añes'),
(3, 'Respaldiza', 'Arespalditza/Respaldiza'),
(3, 'Costera', 'Costera/Opellora'),
(3, 'Echegoyen', 'Etxegoien'),
(3, 'Erbi', 'Erbi'),
(3, 'Izoria', 'Izoria'),
(3, 'Lejarzo', 'Lejarzo/Lexartzu'),
(3, 'Llanteno', 'Llanteno'),
(3, 'Lujo', 'Luxo/Lujo'),
(3, 'Luyando', 'Luiaondo'),
(3, 'Madaria', 'Madaria'),
(3, 'Maroño', 'Maroño'),
(3, 'Menagaray-Beotegui', 'Menagarai-Beotegi'),
(3, 'Menoyo', 'Menoio'),
(3, 'Murga', 'Murga'),
(3, 'Olabezar', 'Olabezar'),
(3, 'Oceca', 'Ozeka'),
(3, 'Quejana', 'Quejana/Kexaa'),
(3, 'Retes de Llanteno', 'Retes de Llanteno'),
(3, 'Salmantón', 'Salmantón'),
(3, 'Sojo', 'Soxo/Sojo'),
(3, 'Zuaza', 'Zuaza/Zuhatza');

-- Barrundia (municipio_id = 23)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(23, 'Audicana', 'Audikana'),
(23, 'Dallo', 'Dallo'),
(23, 'Elguea', 'Elgea'),
(23, 'Etura', 'Etura'),
(23, 'Echávarri-Urtupiña', 'Etxabarri Urtupiña'),
(23, 'Guevara', 'Gebara'),
(23, 'Heredia', 'Heredia'),
(23, 'Hermua', 'Hermua'),
(23, 'Larrea', 'Larrea'),
(23, 'Marieta-Larrínzar', 'Marieta-Larrintzar'),
(23, 'Maturana', 'Maturana'),
(23, 'Mendíjur', 'Mendixur/Mendíjur'),
(23, 'Ozaeta', 'Ozaeta');

-- Berantevilla (municipio_id = 37)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(37, 'Berantevilla', 'Berantevilla'),
(37, 'Lacervilla', 'Lacervilla'),
(37, 'Mijancas', 'Mijancas'),
(37, 'Santa Cruz del Fierro', 'Santa Cruz del Fierro'),
(37, 'Santurde', 'Santurde'),
(37, 'Tobera', 'Tobera');

-- Bernedo (municipio_id = 47)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(47, 'Angostina', 'Angostina'),
(47, 'Arlucea', 'Arluzea'),
(47, 'Bernedo', 'Bernedo'),
(47, 'Marquínez', 'Markinez'),
(47, 'Navarrete', 'Navarrete'),
(47, 'Oquina', 'Okina'),
(47, 'Quintana', 'Quintana'),
(47, 'San Román de Campezo', 'San Román de Campezo/Durruma Kanpezu'),
(47, 'Urarte', 'Urarte'),
(47, 'Urturi', 'Urturi'),
(47, 'Villafría', 'Villafría');

-- Campezo / Kanpezu (municipio_id = 48)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(48, 'Antoñana', 'Antoñana'),
(48, 'Bujanda', 'Bujanda'),
(48, 'Orbiso', 'Orbiso'),
(48, 'Oteo', 'Oteo'),
(48, 'Santa Cruz de Campezo', 'Santa Cruz de Campezo/Santikurutze Kanpezu');

-- Zigoitia (municipio_id = 33)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(33, 'Acosta', 'Acosta/Okoizta'),
(33, 'Apodaca', 'Apodaka'),
(33, 'Berrícano', 'Berrikano'),
(33, 'Buruaga', 'Buruaga'),
(33, 'Cestafe', 'Zestafe'),
(33, 'Echagüen', 'Etxaguen'),
(33, 'Echávarri-Viña', 'Etxabarri Ibiña'),
(33, 'Eribe', 'Eribe'),
(33, 'Gopegui', 'Gopegi'),
(33, 'Letona', 'Letona'),
(33, 'Manurga', 'Manurga'),
(33, 'Mendarózqueta', 'Mendarozketa'),
(33, 'Murúa', 'Murua'),
(33, 'Olano', 'Olano'),
(33, 'Ondátegui', 'Ondategi'),
(33, 'Záitegui', 'Zaitegi');

-- Kuartango (municipio_id = 39)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(39, 'Anda', 'Anda'),
(39, 'Apricano', 'Aprikano'),
(39, 'Echávarri de Cuartango', 'Etxabarri Kuartango'),
(39, 'Jocano', 'Jokano'),
(39, 'Luna', 'Luna'),
(39, 'Marinda', 'Marinda'),
(39, 'Sendadiano', 'Sendadiano'),
(39, 'Ullívarri Cuartango', 'Uribarri Kuartango'),
(39, 'Urbina de Eza', 'Urbina Eza'),
(39, 'Zuazo de Cuartango', 'Zuhatzu Kuartango');

-- Elburgo / Burgelu (municipio_id = 24)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(24, 'Añua', 'Añua'),
(24, 'Arbulo', 'Arbulu'),
(24, 'Argómaniz', 'Argomaniz'),
(24, 'Elburgo', 'Elburgo/Burgelu'),
(24, 'Gáceta', 'Gazeta'),
(24, 'Hijona', 'Hijona/Ixona');

-- Iruña de Oca / Iruña Oka (municipio_id = 38)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(38, 'Montevite', 'Montevite/Mandaita'),
(38, 'Nanclares de la Oca', 'Nanclares de la Oca/Langraiz Oka'),
(38, 'Ollávarre', 'Ollávarre/Olabarri'),
(38, 'Trespuentes', 'Trespuentes'),
(38, 'Víllodas', 'Víllodas/Billoda');

-- Iruraiz-Gauna (municipio_id = 25)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(25, 'Alaiza', 'Alaitza'),
(25, 'Arrieta', 'Arrieta'),
(25, 'Acilu', 'Azilu'),
(25, 'Erenchun', 'Erentxun'),
(25, 'Ezquerecocha', 'Ezkerekotxa'),
(25, 'Gaceo', 'Gazeo'),
(25, 'Gauna', 'Gauna'),
(25, 'Guereñu', 'Gereñu'),
(25, 'Jáuregui', 'Jauregi'),
(25, 'Langarica', 'Langarika'),
(25, 'Trocóniz', 'Trokoniz');

-- Labastida / Bastida (municipio_id = 10)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(10, 'Salinillas de Buradón', 'Salinillas de Buradón/Gatzaga Buradon');

-- Lagrán (municipio_id = 49)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(49, 'Lagrán', 'Lagran'),
(49, 'Pipaón', 'Pipaon'),
(49, 'Villaverde', 'Villaverde');

-- Laguardia (municipio_id = 11)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(11, 'Páganos', 'Páganos');

-- Lantarón (municipio_id = 40)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(40, 'Alcedo', 'Alcedo'),
(40, 'Bergüenda', 'Bergonda/Bergüenda'),
(40, 'Caicedo de Yuso', 'Caicedo de Yuso'),
(40, 'Comunión', 'Comunión/Komunioi'),
(40, 'Fontecha', 'Fontecha'),
(40, 'Leciñana del Camino', 'Leciñana del Camino/Leziñana'),
(40, 'Molinilla', 'Molinilla'),
(40, 'Puentelarrá', 'Puentelarrá/Larrazubi'),
(40, 'Salcedo', 'Salcedo'),
(40, 'Sobrón', 'Sobrón'),
(40, 'Turiso', 'Turiso'),
(40, 'Zubillaga', 'Zubillaga');

-- Oyón-Oion (municipio_id = 17)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(17, 'Barriobusto', 'Barriobusto/Gorrebusto'),
(17, 'Labraza', 'Labraza');

-- Peñacerrada-Urizaharra (municipio_id = 51)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(51, 'Baroja-Zumentu', 'Baroja-Zumentu'),
(51, 'Faido', 'Faido/Faidu'),
(51, 'Loza', 'Loza'),
(51, 'Montoria', 'Montoria'),
(51, 'Payueta', 'Payueta/Pagoeta'),
(51, 'Peñacerrada', 'Peñacerrada-Urizaharra');

-- Ribera Alta / Erriberagoitia (municipio_id = 41)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(41, 'Antezana de la Ribera', 'Antezana de la Ribera'),
(41, 'Anúcita', 'Anuntzeta/Anúcita'),
(41, 'Arreo', 'Arreo'),
(41, 'Artaza-Escota', 'Artaza-Escota/Artatza-Axkoeta'),
(41, 'Barrón', 'Barrón'),
(41, 'Basquiñuelas', 'Basquiñuelas'),
(41, 'Caicedo-Sopeña', 'Caicedo-Sopeña'),
(41, 'Hereña', 'Hereña'),
(41, 'Lasierra', 'Lasierra'),
(41, 'Leciñana de la Oca', 'Leciñana de la Oca'),
(41, 'Morillas', 'Morillas'),
(41, 'Ormijana', 'Ormijana'),
(41, 'Paúl', 'Paúl'),
(41, 'Pobes', 'Pobes'),
(41, 'Subijana-Morillas', 'Subijana-Morillas'),
(41, 'Tuyo', 'Tuyo'),
(41, 'Villabezana', 'Villabezana'),
(41, 'Villaluenga', 'Villaluenga'),
(41, 'Villambrosa', 'Villambrosa'),
(41, 'Viloria', 'Viloria');

-- Ribera Baja / Erriberabeitia (municipio_id = 42)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(42, 'Igay', 'Igay'),
(42, 'Manzanos', 'Manzanos'),
(42, 'Melledes', 'Melledes'),
(42, 'Quintanilla de la Ribera', 'Quintanilla de la Ribera'),
(42, 'Rivabellosa', 'Rivabellosa'),
(42, 'Rivaguda', 'Rivaguda');

-- San Millán / Donemiliaga (municipio_id = 27)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(27, 'Adana', 'Adana'),
(27, 'Aspuru', 'Axpuru'),
(27, 'Vicuña', 'Bikuña/Vicuña'),
(27, 'Eguílaz', 'Eguílaz/Egilatz'),
(27, 'Galarreta', 'Galarreta'),
(27, 'Luzuriaga', 'Luzuriaga'),
(27, 'Mezquía', 'Mezkia'),
(27, 'Munain', 'Munain'),
(27, 'Narvaja', 'Narbaiza'),
(27, 'Ocáriz', 'Okariz'),
(27, 'Ordoñana', 'Ordoñana/Erdoñana'),
(27, 'San Román de San Millán', 'Durruma/San Román de San Millán'),
(27, 'Chinchetru', 'Txintxetru'),
(27, 'Ullíbarri-Jáuregui', 'Ullibarri-Jauregi/Uribarri-Jauregi'),
(27, 'Zuazo de San Millán', 'Zuazo de San Millán/Zuhatzu Donemiliaga');

-- Urkabustaiz (municipio_id = 32)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(32, 'Abecia', 'Abezia'),
(32, 'Abornicano', 'Abornikano'),
(32, 'Belunza', 'Beluntza'),
(32, 'Gujuli-Ondona', 'Goiuri-Ondona'),
(32, 'Inoso', 'Inoso'),
(32, 'Izarra', 'Izarra'),
(32, 'Larrazcueta', 'Larrazkueta'),
(32, 'Oyardo', 'Oiardo'),
(32, 'Unzá-Apreguíndana', 'Untza-Apregindana'),
(32, 'Uzquiano', 'Uzkiano');

-- Valdegovía / Gaubea (municipio_id = 44)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(44, 'Acebedo', 'Acebedo'),
(44, 'Bachicabo', 'Bachicabo'),
(44, 'Barrio', 'Barrio'),
(44, 'Basabe', 'Basabe'),
(44, 'Bóveda', 'Bóveda'),
(44, 'Caranca y Mioma', 'Caranca y Mioma'),
(44, 'Cárcamo', 'Karkamu'),
(44, 'Corro', 'Corro'),
(44, 'Espejo', 'Espejo'),
(44, 'Fresneda', 'Fresneda'),
(44, 'Gurendes-Quejo', 'Gurendes-Quejo'),
(44, 'Nograro', 'Nograro'),
(44, 'Osma', 'Osma'),
(44, 'Pinedo', 'Pinedo'),
(44, 'Quintanilla', 'Quintanilla'),
(44, 'Tobillas', 'Tobillas'),
(44, 'Tuesta', 'Tuesta'),
(44, 'Valderejo', 'Valderejo'),
(44, 'Valluerca', 'Valluerca'),
(44, 'Villamaderne-Bellojín', 'Villamaderne-Bellojín'),
(44, 'Villanañe', 'Villanañe'),
(44, 'Villanueva de Valdegovía', 'Villanueva de Valdegovía');

-- Valle de Arana / Harana (municipio_id = 52)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(52, 'Alda', 'Alda'),
(52, 'Contrasta', 'Kontrasta'),
(52, 'San Vicente de Arana', 'San Vicente de Arana/Done Bikendi Harana'),
(52, 'Ullíbarri-Arana', 'Ullíbarri-Arana/Uribarri Harana');

-- Legutio (municipio_id = 31) - Villarreal de Álava
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(31, 'Elosu', 'Elosu'),
(31, 'Gojáin', 'Goiain'),
(31, 'Villarreal', 'Legutio'),
(31, 'Urbina', 'Urbina'),
(31, 'Urrúnaga', 'Urrunaga');

-- Vitoria (municipio_id = 310)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(310, 'Abechuco', 'Abetxuko'),
(310, 'Aberásturi', 'Aberasturi'),
(310, 'Ali', 'Ehari/Ali'),
(310, 'Amárita', 'Amarita'),
(310, 'Andollu', 'Andollu'),
(310, 'Antezana de Foronda', 'Antezana/Andetxa'),
(310, 'Aránguiz', 'Arangiz'),
(310, 'Arcaute', 'Arkauti/Arcaute'),
(310, 'Arcaya', 'Arkaia'),
(310, 'Arechavaleta', 'Aretxabaleta'),
(310, 'Argandoña', 'Argandoña'),
(310, 'Aríñez', 'Ariñiz/Aríñez'),
(310, 'Armentia', 'Armentia'),
(310, 'Ascarza', 'Askartza'),
(310, 'Asteguieta', 'Astegieta'),
(310, 'Berrosteguieta', 'Berrostegieta'),
(310, 'Betoño', 'Betoño'),
(310, 'Bolívar', 'Bolívar'),
(310, 'Castillo', 'Castillo/Gaztelu'),
(310, 'Cerio', 'Zerio'),
(310, 'Crispijana', 'Krispiña/Crispijana'),
(310, 'Elorriaga', 'Elorriaga'),
(310, 'Esquíbel', 'Eskibel'),
(310, 'Estarrona', 'Estarrona'),
(310, 'Foronda', 'Foronda'),
(310, 'Gamarra Mayor', 'Gamarra Mayor/Gamarra Nagusia'),
(310, 'Gamarra Menor', 'Gamarra Menor'),
(310, 'Gámiz', 'Gamiz'),
(310, 'Gardélegui', 'Gardelegi'),
(310, 'Gobeo', 'Gobeo'),
(310, 'Gomecha', 'Gometxa'),
(310, 'Guereña', 'Gereña'),
(310, 'Hueto Abajo', 'Hueto Abajo/Otobarren'),
(310, 'Hueto Arriba', 'Otogoien/Hueto Arriba'),
(310, 'Ilárraza', 'Ilarratza'),
(310, 'Junguitu', 'Jungitu'),
(310, 'Lasarte', 'Lasarte'),
(310, 'Legarda', 'Legarda'),
(310, 'Lermanda', 'Lermanda'),
(310, 'Lopidana', 'Lopidana'),
(310, 'Lubiano', 'Lubiano'),
(310, 'Margarita', 'Margarita'),
(310, 'Mártioda', 'Martioda'),
(310, 'Matauco', 'Matauko'),
(310, 'Mendiguren', 'Mendiguren'),
(310, 'Mendiola', 'Mendiola'),
(310, 'Mendoza', 'Mendoza'),
(310, 'Miñano Mayor', 'Miñao/Miñano Mayor'),
(310, 'Miñano Menor', 'Miñano Menor/Miñano Gutxia'),
(310, 'Monasterioguren', 'Monasterioguren'),
(310, 'Oreitia', 'Oreitia'),
(310, 'Otazu', 'Otazu'),
(310, 'Retana', 'Retana'),
(310, 'Subijana de Álava', 'Subijana de Álava/Subillana-Gasteiz'),
(310, 'Ullíbarri de los Olleros', 'Ullíbarri de los Olleros/Uribarri Nagusia'),
(310, 'Ullíbarri-Arrazua', 'Ullíbarri-Arrazua'),
(310, 'Ullívarri-Viña', 'Ullíbarri-Viña/Uribarri-Dibiña'),
(310, 'Villafranca de Estíbaliz', 'Villafranca'),
(310, 'Yurre', 'Yurre/Ihurre'),
(310, 'Zuazo de Vitoria', 'Zuazo de Vitoria/Zuhatzu'),
(310, 'Zumelzu', 'Zumeltzu');

-- Zambrana (municipio_id = 45)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(45, 'Berganzo', 'Berganzo'),
(45, 'Ocio', 'Ocio'),
(45, 'Portilla', 'Portilla/Zabalate'),
(45, 'Zambrana', 'Zambrana');

-- Zuia (municipio_id = 34)
INSERT INTO dim_concejos (municipio_id, concejo_nombre, concejo_nombre_oficial) VALUES
(34, 'Amézaga de Zuya', 'Ametzaga Zuia'),
(34, 'Aperregui', 'Aperregi'),
(34, 'Domaiquia', 'Domaikia'),
(34, 'Guillerna', 'Gillerna'),
(34, 'Jugo', 'Jugo'),
(34, 'Luquiano', 'Lukiano'),
(34, 'Marquina', 'Markina'),
(34, 'Murguía', 'Murgia'),
(34, 'Sarría', 'Sarria'),
(34, 'Vitoriano', 'Bitoriano'),
(34, 'Zárate', 'Zarate');

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
