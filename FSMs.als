open util/boolean

sig FSM{
	deterministic : Bool,
	states : some State,
	startState : one State
}

sig State{
	deterministic : Bool,
	transitions : some Transition
}

sig Transition{
	destination : one State,
	label : Label
}

sig Label{
}

fact stateRules{
	//all states belong to some FSM
	all s : State | s in FSM.states

	//all start states belong to an FSM's state set
	all f : FSM | f.startState in f.states
	
	//all states have at least one outgoing transition
	all s : State | #s.transitions > 0
	
	//all states have at least one incoming transition
	all s : State | s in Transition.destination
}

fact transitionRules{
	//All transitions are owned by at least one state
	all t : Transition | one s : State | t in s.transitions
}

fact determinism{
	//If the set of all transitions from a state is larger than the set of all of those transitions'
	// labels, then we have Nondeterministic transitions. (Pigeonhole principle!)
	all s : State | (#s.transitions.label < #s.transitions) => (s.deterministic = False)
	all s : State | (#s.transitions.label >= #s.transitions) => (s.deterministic = True)

	//FSMs are deterministic if all of their states are deterministic
	all f : FSM | all s : f.states | (s.deterministic = True) => (f.deterministic = True)

	//FSMs are nondeterministic if any of their states are nondeterministic
	all f : FSM | some s : f.states | (s.deterministic = False) => (f.deterministic = False)

	//Forcibly DFAs
	//Labels are not shared between transitions
	all l : Label | one t : Transition | (l = t.label)

	//Forcibly NFAs
//	some s : State | s.deterministic = False
}

fact limitSize{
	#FSM = 1
}

pred Show{}

run Show for 4
