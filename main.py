import sys
import glob
import json
from pathlib import Path
from google_trans_new import google_translator
import re

translator = google_translator()


def startTranslate(srcFolder, desFolder, srcLang, desLang):

    Path(desFolder).mkdir(parents=True, exist_ok=True)

    files = []
    for file in glob.glob(srcFolder+"/*.arb"):
        files.append(file)

    for file in files:
        with open(file, encoding="utf8") as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                if key.find('@') == -1:
                    data[key] = _translateAndProcess(
                        data[key], srcLang, desLang)
            with open(desFolder+'/'+file[file.rindex('\\')+1:], 'w+',  encoding='utf8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4,)


def _translateAndProcess(text, srcLang, desLang):
    translatedText = translator.translate(
        text, lang_src=srcLang, lang_tgt=desLang).strip()
    if translatedText.find('{') == -1:
        return translatedText
    else:
        pattern = re.compile(r'{(.+?)}')
        srcVars = re.findall(pattern, text)
        desVars = re.findall(pattern, translatedText)
        for i in range(len(srcVars)):
            translatedText = translatedText.replace(desVars[i], srcVars[i])
        return translatedText


if __name__ == "__main__":
    if len(sys.argv) == 5:
        srcFolder = sys.argv[1]
        desFolder = sys.argv[2]
        srcLang = sys.argv[3]
        desLang = sys.argv[4]
        startTranslate(srcFolder, desFolder, srcLang, desLang)
    else:
        print("Invalid argument")
