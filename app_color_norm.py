from color_normalization.parser import create_parser
from utils.utilities import set_random_seed
from color_normalization import ColorNormalization

if __name__ == "__main__":
    parser = create_parser()
    config = parser.parse_args()
    set_random_seed(config.seed)
    cn = ColorNormalization(config)
    cn.run()
