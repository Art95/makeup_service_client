sudo docker run --name makeup_service_client --network host --device=/dev/video0:/dev/video0 \
                -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v $PWD:/app -det -it abaraniuk/makeup_service:client
sudo docker exec -i makeup_service_client bash -c "cd /app/ && pip3 install -r requirements.txt ."
sudo docker exec -i makeup_service_client bash -c "python3 /app/makeup_service_client/client/app.py"