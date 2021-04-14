import argparse
import json
import numpy as np
import os
from collections import namedtuple
from typing import NamedTuple

def my_divmod(
  dividend: float,
  divisor: float) -> NamedTuple(
    'MyDivmodOutput',
    [
      ('quotient', float),
      ('remainder', float),
      ('mlpipeline_ui_metadata', 'UI_metadata'),
      ('mlpipeline_metrics', 'Metrics')
    ]):
    
    '''Divides two numbers and calculate  the quotient and remainder'''

    # Import the numpy package inside the component function


    # Define a helper function
    def divmod_helper(dividend, divisor):
        return np.divmod(dividend, divisor)

    (quotient, remainder) = divmod_helper(dividend, divisor)

    # Export a sample tensorboard
    metadata = {
      'outputs' : [{
        'type': 'tensorboard',
        'source': 'gs://ml-pipeline-dataset/tensorboard-train',
      }]
    }

    # Export two metrics
    metrics = {
      'metrics': [{
          'name': 'quotient',
          'numberValue':  float(quotient),
        },{
          'name': 'remainder',
          'numberValue':  float(remainder),
        }]}

    divmod_output = namedtuple('MyDivmodOutput',
        ['quotient', 'remainder', 'mlpipeline_ui_metadata',
         'mlpipeline_metrics'])
    return divmod_output(quotient, remainder, json.dumps(metadata),
                         json.dumps(metrics))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dividend', type=float)
    parser.add_argument('--divisor', type=float)
    parser.add_argument("--output_paths", dest="_output_paths", type=str, nargs=4)
    _parsed_args = vars(parser.parse_args())
    output_files = _parsed_args.pop("_output_paths", [])

    args = parser.parse_args()

    outputs = my_divmod(args.dividend, args.divisor)

    for idx, output_file in enumerate(output_files):
        try:
            os.makedirs(os.path.dirname(output_file))
        except OSError:
            pass
        with open(output_file, 'w') as f:
            f.write(str(outputs[idx]))
