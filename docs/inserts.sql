INSERT INTO university_paises(codigo, nombre) VALUES (1, 'Pais');

INSERT INTO university_departamentos(codigo, nombre, cod_pais_id) 
VALUES 
(1, 'Departamento', 1);

INSERT INTO university_ciudades(codigo, nombre, cod_dpto_id) 
VALUES 
(1, 'Ciudad', 1);

INSERT INTO university_sedes (codigo, nombre, cod_ciudad_id)
VALUES
(1, 'Sede', 1);

INSERT INTO university_tipos_contratacion (nombre)
VALUES
('Contratación');

INSERT INTO university_tipos_empleado (nombre)
VALUES
('profesor'),
('administrativo'),
('director');

// ------------------------------
INSERT INTO university_areas (codigo, nombre, cod_facultades, id_coordinador)
VALUES
(1, 'Area', 1, 1);
// ------------------------------

INSERT INTO university_areas (codigo, nombre)
VALUES
(1, 'Area');

INSERT INTO university_programas (codigo, nombre, cod_areas_id)
VALUES
(1, 'Programa', 1);

// ------------------------------
INSERT INTO university_facultades (codigo, nombre, ubicacion, nro_telefono, id_decano)
VALUES
(1, 'Facultad', 'Ubicacion', '123456', 1);
// ------------------------------

INSERT INTO university_facultades (codigo, nombre, ubicacion, nro_telefono)
VALUES
(1, 'Facultad', 'Ubicacion', '123456');

INSERT INTO university_empleados (identificacion, nombres, apellidos, email, tipo_contratacion_id, tipo_empleado_id, cod_facultad_id, cod_sede_id, lugar_nacimiento_id)
VALUES
('1096800052', 'Silem Nabib', 'Villa Contreras', 'silemnabib@gmail.com', 'Contratación', 'profesor', 1, 1, 1);