portList=(5000)
noOfPorts=$1
for (( i=0; i<$noOfPorts-1; i++ ))
do
	let temp=${portList[$i]}+1
	portList+=($temp)
done
echo ${portList[@]}
for (( i=0; i<$noOfPorts; i++ ))
do
	echo "Opening port ${portList[$i]}"
	gnome-terminal -- /bin/bash -c "python3 node.py ${portList[$i]} $noOfPorts"
done
