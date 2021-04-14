import argparse
import os

def add(a: float, b: float) -> float:
  '''Calculates sum of two arguments'''
  return a + b


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--a', type=float)
    parser.add_argument('--b', type=float)
    parser.add_argument("--output_path", type=str)

    args = parser.parse_args()
    result = add(args.a, args.b)

    try:
        os.makedirs(os.path.dirname(args.output_path))
        with open(args.output_path, 'w') as f:
            f.write(str(result))
    except OSError:
        pass
