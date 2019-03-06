import os
import argparse
import requests
import tempfile
import gzip
import shutil
import multiprocessing as mp
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from showdata.models import Specie, Kingdom, Entry


class Command(BaseCommand):
    help = 'Importa arquivo de dados de DNA / RNA.'
    FILEPATH = os.path.join(tempfile.gettempdir(), '.{}'.format(hash(os.times())))

    def split_data(self, line):
        access_id, data = line.split(' ', 1)
        datalist = data.split(';')
        kingdom = datalist[0]
        specie = datalist[-1]
        return access_id, kingdom, specie


    def get_data(self, filename, maxrecords):
        records = []
        with open(filename, 'r') as f:
            line = f.readline()
            records_count = 0
            while line:
                if line.startswith('>'):
                    record = {}
                    access_id, kingdom, specie = self.split_data(line)
                    record['access_id'] = access_id[1:]
                    record['kingdom'] = kingdom
                    record['specie'] = specie.rstrip()
                    record['sequence'] = f.readline().rstrip()
                    records.append(record)
                    records_count += 1 
                    if records_count == maxrecords:
                        break
                line = f.readline()
        return records            


    def download_file(self, url, file_path):
        local_filename = url.split('/')[-1]
        local_filename = os.path.join(file_path, local_filename)
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)
        return local_filename


    def gunzip(self, source_file, block_size=65536):
        dest_file = os.path.splitext(source_file)[0]
        with gzip.open(source_file, 'rb') as pack_file, open(dest_file, 'wb') as unpack_file:
            shutil.copyfileobj(pack_file, unpack_file, block_size)
        return dest_file    


    def save_record(self, record):
        specie, _ = Specie.objects.get_or_create(label=record['specie'])
        kingdom, _ = Kingdom.objects.get_or_create(label=record['kingdom'])
        entry = Entry(access_id=record['access_id'], kingdom=kingdom, specie=specie, sequence=record['sequence'])
        specie.save()
        kingdom.save()
        entry.save()

    @transaction.atomic
    def save_data(self, data):
        for record in data:
            self.save_record(record)


    def add_arguments(self, parser):
         parser.add_argument('dnadata', type=str, help='Link para download do arquivo de dados de DNA / RNA.')


    def handle(self, *args, **kwargs):
        URL = kwargs['dnadata']
        FILEPATH = os.path.join(tempfile.gettempdir(), '.{}'.format(hash(os.times())))
        MAXRECORDS = 5000

        os.makedirs(FILEPATH)

        data_file = self.download_file(URL, FILEPATH)
        data_file = self.gunzip(data_file)

        data = self.get_data(data_file, MAXRECORDS)
        self.save_data(data)
