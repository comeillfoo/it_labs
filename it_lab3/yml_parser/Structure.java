class Value {

}

class Sequence extends Value implements Iterable {
	private List<Sequence> subseq = new List<Sequence>();
	private List<Mapping> submap = new List<Mapping>();
	private List<Double> subnum = new List<Double>();
	private List<String> substr = new List<String>();
	private List<List<Value>> seq = new List<List<Value>>();
	public Sequence(Sequence seq) {
		for el in seq {
			if (el instanceof(Sequence))
				subseq.append(el);
			else if (el instanceof(Mapping))
				submap.append(el);
			else if (el instanceof(Double))
				subnum.append(el);
			else if (el instanceof(String) || el instanceof(Scalar))
				substr.append(el.ToString());
		}
		this.seq.append(this.subseq);
		this.seq.append(this.submap);
		this.seq.append(this.subnum);
		this.seq.append(this.substr);
	}

}

class Mapping extends Value {
	private Key key;
	private Value value;
	public Mapping(Key _key, Value _value) {
		this.key = _key;
		this.value = _value;
	}
}

class Mappings {
	private List<Key> keys = new List<Key>();
	private List<Value> values = new List<Value>();
	
	public Mappings(List<Mapping> maps) {
	}
}