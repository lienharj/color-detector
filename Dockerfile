FROM duckietown/dt-duckiebot-interface:daffy-arm32v7

WORKDIR /color_detector

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY color_detector.py .

CMD python ./color_detector.py
