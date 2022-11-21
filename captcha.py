from helper import HelperFunctions as hf


class Captcha(object):
    def __init__(self, dict_path):
        self.hashDict = hf.loadAndComputeHashes(dict_path)
        pass

    def __call__(self, im_path, save_path):
        """
        Algo for inference
        args:
            im_path: .jpg image path to load and to infer
            save_path: output file path to save the one-line outcome
        """
        read_letters = hf.readImg(im_path, self.hashDict)
        with open(save_path, 'w') as fp:
            fp.write(''.join(read_letters))

        pass
