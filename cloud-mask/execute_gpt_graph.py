import multiprocessing
import os
import time
import zipfile
from bs4 import BeautifulSoup
import subprocess
import matplotlib.pyplot as plt

GPT_PATH = "/home/flavio/esa-snap/bin/gpt" # percorso all'eseguibile gpt di SNAP
TILES_DIR = "/mnt/DATA/satellites_products/T33TUG/" # cartella con i prodotti
OUTPUT_DIR = "/mnt/DATA/satellites_products/T33TUG/outputs/" # cartella con il prodotto in output
CPU_COUNT = multiprocessing.cpu_count()
META_FILENAME = 'MTD_MSIL2A.xml'
MASKED_WORKFLOW = 'masked_ndvi.xml'
UNMASKED_WORKFLOW = 'unmasked_ndvi.xml'

def main():


    x_axis = []
    y1_axis = []
    y2_axis = []
    print('---START---')
    for tilePath in os.listdir(TILES_DIR):
        if tilePath.endswith('.zip'):
            fullTilePath = os.path.join(TILES_DIR,tilePath)
            tile = zipfile.ZipFile(fullTilePath, 'r')
            metaZipPath = next(path for path in tile.namelist() if path.find(META_FILENAME) > 0)
            with tile.open(metaZipPath, 'r') as metadataFile:
                metadata = BeautifulSoup(metadataFile, "xml")
            
            highCloudsPercentage = metadata.find('HIGH_PROBA_CLOUDS_PERCENTAGE').text
            # mediumCloudsPercentage = metadata.find('MEDIUM_PROBA_CLOUDS_PERCENTAGE').text
            x_axis.append(round(float(highCloudsPercentage),2))
            print(f'---{tilePath}---')
            print(f'High Probability Clouds Percentage: {highCloudsPercentage}')
            # print(f'Medium Probability Clouds Percentage: {mediumCloudsPercentage}\n')
            start_time = time.time()
            maskedOutput = subprocess.run(
                [
                GPT_PATH,
                os.path.join(os.getcwd(),MASKED_WORKFLOW),
                f'-SsourceProduct={fullTilePath}',
                '-t',
                os.path.join(OUTPUT_DIR, "output.dim"),
                '-q',
                str(CPU_COUNT),
                '-x'],
                capture_output=True, text=True, cwd=os.getcwd())
            elapsed_time = time.time() - start_time
            y1_axis.append(round(elapsed_time,2))
            print(f'Masked compute time: {elapsed_time}')
            start_time = time.time()
            unamaskedOutput = subprocess.run(
                [
                GPT_PATH,
                os.path.join(os.getcwd(),UNMASKED_WORKFLOW),
                f'-SsourceProduct={fullTilePath}',
                '-t',
                os.path.join(OUTPUT_DIR, "output.dim"),
                '-q',
                str(CPU_COUNT),
                '-x'],
                capture_output=True, text=True, cwd=os.getcwd())
            elapsed_time = time.time() - start_time
            y2_axis.append(round(elapsed_time,2))
            print(f'Unmasked compute time: {elapsed_time}')

    print('---END---')


    x_axis, y1_axis, y2_axis = zip(*sorted(zip(x_axis,y1_axis,y2_axis)))

    fig, ax = plt.subplots()

    ax.plot(x_axis,y1_axis, color='red', marker='o')
    ax.plot(x_axis,y2_axis, color='blue', marker='x')
    plt.title('Compute time comparison')
    plt.xlabel('High Probability Clouds Percentage (%)')
    plt.ylabel('Computing Time (sec)')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
