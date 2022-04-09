import argparse
import multiprocessing
import os
import time

GPT_PATH = "" # percorso all'eseguibile gpt di SNAP
FRAMES_DIR = "" # cartella con i 4 prodotti sentinel-2 in input
OUTPUT_DIR = "" # cartella con il prodotto in output
CPU_COUNT = multiprocessing.cpu_count()


def main():
    parser = argparse.ArgumentParser(
        description='Execute a gpt graph on a single frame')
    parser.add_argument('gpt_graph', nargs=1)
    args = parser.parse_args()
    graph_xml_path = args.gpt_graph[0]

    zipped_frames_list = [
        f'{FRAMES_DIR}/T33TTG/S2A_MSIL2A_20220306T100031_N0400_R122_T33TTG_20220306T120714.zip',
        f'{FRAMES_DIR}/T33TTG/S2A_MSIL2A_20220316T100031_N0400_R122_T33TTG_20220316T134748.zip',
        f'{FRAMES_DIR}/T33TUG/S2A_MSIL2A_20220306T100031_N0400_R122_T33TUG_20220306T120714.zip',
        f'{FRAMES_DIR}/T33TUG/S2A_MSIL2A_20220316T100031_N0400_R122_T33TUG_20220316T134748.zip',
    ]

    command = GPT_PATH + ' ' \
        + graph_xml_path \
        + ' -Pin_a1=' + zipped_frames_list[0] \
        + ' -Pin_a2=' + zipped_frames_list[1] \
        + ' -Pin_b1=' + zipped_frames_list[2] \
        + ' -Pin_b2=' + zipped_frames_list[3] \
        + ' -t ' + os.path.join(OUTPUT_DIR, "sentinel2-ndvi_" + str(time.time())) + ".dim" \
        + ' -q ' + str(CPU_COUNT) + ' -x '
    
    print(command)
    
    start_time = time.time()
    #os.system(command)
    print('Elapsed time: %s seconds' % (time.time() - start_time))


if __name__ == "__main__":
    main()
