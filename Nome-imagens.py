from osgeo import gdal, osr
import os

shape_path = '/home/grodigheri/git/Trabalho-BDGeo/Shapes/MESO_RS_NE/ExportMeso_Output.shp'
path = '/home/grodigheri/git/Trabalho-BDGeo/Imagens_NDVI(2)/'

files = os.listdir(path)
print(files)

for filename in files:
    name = path + filename
    print(name)
        
    # Abre a imagem que será utilizada
    dataset = gdal.Open(name)

    # # Verifica a projeção de uma imagem MOD13Q1
    # projInfo = dataset.GetProjection()
    # spatialRef = osr.SpatialReference()
    # spatialRef.ImportFromWkt(projInfo)
    # print("Imagem original: " + str(spatialRef))

    # Reprojeta a imagem
    name_repro = path + 'proj' + filename
    print(name_repro)
    dsrep = gdal.Warp(name_repro, 
                        dataset,
                        dstSRS='EPSG:4674') #SIRGAS 2000
    print("Imagem reprojetada: " + str(dsrep.GetProjection()))
    dsrep = None

    # Corta a imagem com a shape
    name_clip = path + 'clip' + filename
    print(name_clip)
    dsclip = gdal.Warp(name_clip, 
                        name_repro, 
                        cutlineDSName = shape_path, 
                        cropToCutline = True,
                        dstNodata = 0)

    # Fechas as imagens utilizadas
    dsclip = None
    dataset = None

files_clip = [f for f in files if 'clip' in f]
print(files_clip)

os.chdir(path)

for filename in files_clip:
    print('--------------------------------------------------------')
    name_stif = filename[0:12]
    print(name_stif)

    # Gera o sql e adiciona no banco
    cmd1 = 'raster2pgsql -I -C -M -s 4674 ' + filename + ' -t 100x100 public.' + name_stif + ' > ' + name_stif +'.sql'
    print(cmd1)
    os.system(cmd1)

    cmd2 = 'PGPASSWORD=secreto psql -U postgres -h localhost -p 5432 -d trabalhobd -f ' + name_stif +'.sql'
    print(cmd2)
    os.system(cmd2)
