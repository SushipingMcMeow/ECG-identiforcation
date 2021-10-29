ECG_For_Biometrics_v3 is an attempt to use data from an electrocardiogram (ECG) as a form of bioidentiforcation.
It takes in ECG data from many different sources within a file, and runs a specified number of tests.
In each test, it first selects a single heartbeat from one of the provided sources.
This heartbeat is then pared up with an id that is either from the same source or a different source depending on whether it is a positive or negative test.
For every heartbeat in every profile, the test heartbeat is compared using Dynamic Time Warp and a warp area is generated (see https://dynamictimewarping.github.io/py-api/html/api/dtw.warpArea.html#dtw.warpArea).
The 5 profile heartbeats with the lowest warp areas are then subjected to an algorithm similar to KNN.
Here the profile with the most heartbeats within the 5 is generally selected to be the true profile.
If there's a tie, the profile with the lowest score is selected to be the true profile.
The id of this selected profile is then compared with the pared id.
Depending on the results, the test will return either TN, TP, FN or FP
These tests are done a number of times and the results will build up a confussion matrix where the results can be analysed.

input variables:
	Dir: Directory of the ECG data.
	signal_freq: Signal frequency used by the dataset (1000 for CYBHi).
	profilesize: Number of heartbeats to compare within a single profile.
	numOfprofiles: Number of profiles to be used in each test.
	numOfTests: Number of tests to be conducted.

functions:
	importFiles:
		Used to get a random sample of ECG data file names from the ecg data directory.
		input:
			amount: Number of files name to be returned.
		output: List of strings of file names
	runTest:
		Runs a single test to see whether a question subject is equal to a test subject:
		input:
			participants: List of profile objects to compare the test subject to.
			testSubject: A subject object with an id and a single heartbeat signal. This is what is going to be compared with every other heartbeat within all the profiles.
			questionSubject: A string of a single id that the which the algorithm is going to see if it belongs to the test subject.
		output: a string of either TP, TN, FP or FN
	subjectArray:
		Makes a list of profile objects to be used for testing.
		input:
			data: List of ECG data file names.
		output: A list of profile objects
	shrinkTo:
		Gets a random but specified amount of ECG data.
		input:
			data: An array of ECG data to be shrunk.
			amount: Size the ECG array will be shrunk to.
	getData:
		Gets the ECG data from a stated file and removes the noise from it
		input:
			fileName: String of the target file name.
		output: Returns a filterd array of ECG data.
	rpeakToRpeak:
		Selects a single heartbeat en some ECG data from one r peak to the next r peak
		input:
			data: An array of ECG data.
			rpeaks: List of locations of r peaks within the data.
			rpeak: int of the location of one the first r peak to be returned.
		output: An array of the ECG data of a single heartbeat.
	singleHB:
		Selects a random heartbeat from an array of ECG data.
		input:
			data: Array of ECG data from a a file.
		output: ECG data array of a single heartbeat
	getHeartBeats:
		Generates a list of random heartbeats from within an ECG data array.
		input:
			data: Array of ECG data from a a file.
			amount: Int of the number of heartbeats to be returned.
		output: a list of data arrays of single heart beats
	generateSubject:
		Makes a subject object with an id and an array of a single random heartbeat.
		input:
			fileName: String of the name of the target file
		output: Subject object with an id and an array of a single random heartbeat



object classes:
	profile:
		ID: String used to identify which data file the data came from.
		HBs: A list containing signal data arrays from a number of heartbeats from the same file.
		     profilesize determines how many heartbeats each profile contains
	subject:
		ID: String used to identify which data file the data came from.
		HeartBeat: A single heartbeat array contained as ECG data.