# toncli-contest

To run this as a container, go to the cloned repo path and run to build the image

```docker build -t toncli-api .```

To run the container you should execute : 

```docker run -d -p 5000:5000 --name toncli-api toncli-api```

Check afterwards whether the http://127.0.0.1:5000/ api returns any results
