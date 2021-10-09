import yaml

def main(cfg_path='./config.yaml'):
    with open(cfg_path, 'r') as f:
        cfg = yaml.safe_load(f)
    for action in cfg['actions']:
        module = __import__(action)
        module.main(cfg[action])

if __name__ == '__main__':
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument('-c', '--config', type=str, default='./config.yaml')

    args = args.parse_args()
    main(args.config)