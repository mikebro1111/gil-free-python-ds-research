import numpy as np
import pandas as pd
import threading
from queue import Queue
from src.data_processing.text_cleaner import clean_text


class ETLWorker(threading.Thread):
    """
    A worker thread that performs ETL (Extract, Transform, Load) operations.

    Attributes:
        input (Queue): The input queue where data chunks are received.
        output (Queue): The output queue where processed data chunks are sent.
    """

    def __init__(self, input_queue, output_queue):
        """
        Initializes the ETL worker thread.

        Args:
            input_queue (Queue): The input queue where data chunks are received.
            output_queue (Queue): The output queue where processed data chunks are sent.
        """
        super().__init__()
        self.input = input_queue
        self.output = output_queue

    def run(self):
        """
        Runs the ETL worker thread.

        This method continuously receives data chunks from the input queue, performs
        transformation operations, and sends the processed data chunks to the output queue.
        """
        while True:
            data = self.input.get()
            if data is None:  # Signal to stop
                self.input.task_done()
                break

            # Transformation stage
            data['clean_text'] = data['text'].apply(clean_text)
            data['text_length'] = data['clean_text'].str.len()

            self.output.put(data)
            self.input.task_done()


def run_etl_pipeline(data_path, num_workers=4):
    """
    Runs the ETL pipeline using a pool of worker threads.

    Args:
        data_path (str): The path to the input data file.
        num_workers (int, optional): The number of worker threads to use. Defaults to 4.

    Returns:
        pd.DataFrame: The concatenated results of the ETL pipeline.
    """
    input_queue = Queue()
    output_queue = Queue()

    # Initialize workers
    workers = []
    for _ in range(num_workers):
        w = ETLWorker(input_queue, output_queue)
        w.start()
        workers.append(w)

    # Load stage
    chunks = pd.read_csv(data_path, chunksize=1000)
    for chunk in chunks:
        input_queue.put(chunk)

    # Signal to stop
    for _ in range(num_workers):
        input_queue.put(None)

    # Wait for completion
    input_queue.join()

    # Aggregate results
    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    return pd.concat(results)