"""

Streaming Process: Uses port 9999

Create a fake stream of data. 
Use temperature data from the batch process.

Reverse the order of the rows to read OLDEST data first.

Important! 

We'll stream forever - or until we read the end of the file. 
Use use Ctrl-C to stop. (Hit Control key and c key at the same time.)

Explore more at 
https://wiki.python.org/moin/UdpCommunication

"""

# Import from Python Standard Library
import csv
import socket
import time
import logging

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "us-counties.csv"
OUTPUT_FILE_NAME = "out99.txt"

# Prepare message from a row of data
def prepare_message_from_row(row):
    date, county, state, fips, cases, death = row
    fstring_message = f"[{date}, {county}, {state}, {fips}, {cases}, {death}]"
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE

# Stream and write data
def stream_row(input_file_name, address_tuple, num_rows=9):
    logging.info(f"Starting to stream and write {num_rows} rows of data from {input_file_name} to {address_tuple}.")

    sock_object = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Open input file
    with open(input_file_name, "r") as input_file:
        logging.info(f"Opened for reading: {input_file_name}.")
        reader = csv.reader(input_file, delimiter=",")
        header = next(reader)
        logging.info(f"Skipped header row: {header}")

        # Open output file
        with open(OUTPUT_FILE_NAME, "w", newline="") as output_file:
            logging.info(f"Opened for writing: {OUTPUT_FILE_NAME}.")
            writer = csv.writer(output_file, delimiter=",")

            # Write the header row
            writer.writerow(header)

            # Stream and write each row
            for _ in range(num_rows):
                row = next(reader, None)
                if row is None:
                    break

                # Prepare message and send via UDP
                MESSAGE = prepare_message_from_row(row)
                sock_object.sendto(MESSAGE, address_tuple)
                logging.info(f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")
                
                # Write the row to the output file
                writer.writerow(row)
                
                # Wait before sending the next message
                time.sleep(3)

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, ADDRESS_TUPLE, num_rows=99)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")