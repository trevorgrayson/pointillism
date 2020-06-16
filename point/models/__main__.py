import logging
import argparse
from . import GitHubUser

MODELS = {
   'user': GitHubUser
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser("pointillism model cli")
    parser.add_argument('model',
                        help="model name")
    parser.add_argument('key',
                        help="unique lookup id")
    args = parser.parse_args()

    result = None
    model = MODELS.get(args.model)
    if model:
        logging.info(f"Using {model}")
        result = model.find(cn=args.key)

    print(result[0].git_token)
