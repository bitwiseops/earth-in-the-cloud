import argparse
import multiprocessing
import os
import time

GPT_PATH = "/home/snap/bin/gpt" # percorso all'eseguibile gpt di SNAP
FRAMES_DIR = "/mnt/DATA/Uni/dati_satelliti/" # cartella con i 4 prodotti sentinel-2 in input
OUTPUT_DIR = "/mnt/DATA/Uni/dati_satelliti/outputs/" # cartella con il prodotto in output
CPU_COUNT = multiprocessing.cpu_count()


def main():
    parser = argparse.ArgumentParser(
        description='Execute a gpt graph on a single frame')
    parser.add_argument('gpt_graph', nargs=1)
    args = parser.parse_args()
    graph_xml_path = args.gpt_graph[0]

    zipped_frames_list = []

    for frame_zip in os.listdir(FRAMES_DIR):
        if frame_zip.endswith('.zip'):
            zipped_frames_list.append(os.path.join(FRAMES_DIR, frame_zip))

    print(zipped_frames_list)

    command = GPT_PATH + ' ' \
        + graph_xml_path \
        + ' -Pin1=' + zipped_frames_list[0] \
        + ' -Pin2=' + zipped_frames_list[1] \
        + ' -Pin3=' + zipped_frames_list[2] \
        + ' -Pin4=' + zipped_frames_list[3] \
        + ' -t ' + os.path.join(OUTPUT_DIR, "sentinel2-mosaic_" + str(time.time())) + ".dim" \
        + ' -q ' + str(CPU_COUNT) + ' -x '
    
    print(command)
    
    start_time = time.time()
    os.system(command)
    print('Elapsed time: %s seconds' % (time.time() - start_time))


if __name__ == "__main__":
    main()
