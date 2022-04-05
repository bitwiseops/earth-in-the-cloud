# earth-in-the-cloud

## mosaicing

1. Scarica i prodotti di input
   - Il test e' stato eseguito sui seguenti 4 prodotti
     - PDGS Processing Baseline number: N0400
     - Relative Orbit number: R122
     - Tile number field: T32TQM, T32TQN, T33TUG, T33TUH
2. Aggiorna il codice con i percorsi corretti
3. Avvia lo script `python3 ./mosaicing/execute_gpt_graph.py ./mosaicing/sentinel2-mosaic.xml`
