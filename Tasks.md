Each task is scored from 0 to 100 points depending on number of passed tests.
Each get method execution is limited by 100 000 000 (hundred millions) of gas units.
The participant can send solutions and receive the result after short evaluation delay any number of times, but not more than 5 times per hour. The best submitted solution (with highest total score over all 5 tasks) will be used to determine final rank.
The organizers of the competition reserve the right to publish participants solutions with usernames (decided by participants themselves) after the contest.

Solution should only contain 5 files: 1.fc, 2.fc, 3.fc, 4.fc and 5.fc.

In the same directory with contestant solutions stdlib.fc (from [ton-blochcain repository](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/stdlib.fc)) and `typehelpers.fc` (see below all tasks) will be presented. Contestants are welcome to `include` those files (note that functions declared in solution should not overwrite those in stdlib and typehelpers.fc)

Gas-usage will not affect the ranking. Signatures of all functions described in the task conditions should not be changed.

1.
```
{-

  TASK 1 - Greatest common divisor
  Write the method that calculates greater common divisor for two integers greater 
  or equal to 1 and less than 1048576.
-}

() recv_internal() {
}

(int) gcd(int a, int b) method_id {
}
```
2.
```
{-

  TASK 2 - Message validation.
  Write the method that checks that cell contains valid message
  in accordance to https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb#L155
  Note, tests will only cover valid and invalid MessageAny objects,
  valid MessageRelaxed (which are not simultaneously MessageAny) will not be presented
  If message is invalid for any reason - method should return (0, null), otherwise 
  it should return (-1, [slice src, slice dest, int amount] ), where src, dest and 
  amount represents source of the message, destination of the message and attached 
  amount of TONs. If any of those values are not presented (or presented as 
  addr_none slice) in the message cell - they should be substituted with null.
  It is guaranteed that for all tests any HashmapE datatype in message structure 
  is empty hashmaps (has hme_empty constructor).
-}

() recv_internal() {
}

(int, tuple) validate_message(cell message) method_id {
}

```
3.
```
{-

  TASK 3 - (De)Serialize to Cell
  Write the methods
    a) for serialization of tuple of arbitrary values of different types to Cell
    b) for deserialization of Cell created by method above to original tuple
  
  `serialize` method gets as input tuple with arbitrary number of elements from 0 
  to 128 (both 0 and 128 elements are allowed) and outputs Cell. Elements of the 
  tuple may be `null`, `int`, `cell`, `slice`, `tuple` (with the same limitations 
  as original tuple). It is guaranteed that the maximum nesting level of tuples 
  is less than 4 and total number of elements less than 1024.
  `deserialize` method gets a cell produced by `serialize` method and should 
  return origin tuple.
  
  Note, for illustrative purposes`serialize_t3` and `deserialize_t3` functions
  which serialize and deserialize tuple with exactly 3 elements 
  (only null, int, cell and slice are supportd) to/from a cell  have been added.
  Participants are free to not use logic from there and come up with their own
  implementations
-}


() recv_internal() {
}

(cell) serialize(tuple values) method_id {
}

(tuple) deserialize(cell serialized) method_id {
}

;; ==== Illustrative material ====
builder serialize_element(builder b, var x) {
  if(is_null(x)) {
    b~store_uint(0,3);
  }
  if(is_int(x)) {
    ;; before this point compiler do not know true type of x
    ;; force it to be int
    int i_x = force_cast_to_int(x);
    b = b.store_uint(1,3).store_int(i_x, 257);
  }
  if(is_cell(x)) {
    ;; before this point compiler do not know true type of x
    ;; force it to be cell
    cell c_x = force_cast_to_cell(x);
    b = b.store_uint(2,3).store_ref(c_x);
  }
  if(is_slice(x)) {
    ;; before this point compiler do not know true type of x
    ;; force it to be slice
    slice s_x = force_cast_to_slice(x);
    b = b.store_uint(3,3).store_ref(begin_cell().store_slice(s_x).end_cell());
  }
  return b;
}

(slice, tuple) deserialize_element_to_tuple(slice s, tuple t) {
  int element_type = s~load_uint(3);
  if(element_type == 0) {
    t~tpush(null());
  }
  if(element_type == 1) {
    t~tpush(s~load_int(257));
  }
  if(element_type == 2) {
    t~tpush(s~load_ref());
  }
  if(element_type == 3) {
    t~tpush(s~load_ref().begin_parse());
  }
  return (s,t);
}

cell serialize_t3(tuple three_elements) method_id {
  throw_unless(777, three_elements.tuple_length() == 3);
  builder srl = begin_cell();
  srl = serialize_element(srl, three_elements.first());
  srl = serialize_element(srl, three_elements.second());
  srl = serialize_element(srl, three_elements.third());
  return srl.end_cell();
}

tuple deserialize_t3(cell sc) method_id {
  slice s = sc.begin_parse();
  tuple t = empty_tuple();
  repeat (3) {
    (s,t) = deserialize_element_to_tuple(s,t);
  }
  return t;
}

```
4.
```
{-

  TASK 4 - Merge hashmaps (dictionaries)
  Write the method that merges two hashmaps into one. When keys of hashmaps 
  interesect - values from first hashmap should be used, while discarded 
  key/value pairs should be stored into separate hashmap.
  Method should return two hashmaps (merged_dict, discared_dict). If any 
  of resulting hashmaps is empty it should be represented by `null` value.
  Hashmap key length is 256 bit. Each hashmap has at most 256 elements.
-}

() recv_internal() {
}

(cell, cell) merge_hashmaps(cell dict1, cell dict2) method_id {
}

```
5.

```
{-

  TASK 5 - Address encoder
  Write the method that for any valid MsgAddressInt with addr_std constructor 
  without anycast
  (see https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb#L105)
 returns the slice that contain ASCII encoded base64url user-friendly bouncable 
 address (without test-only flag), see https://ton.org/docs/#/howto/step-by-step?id=_1-smart-contract-addresses
-}

() recv_internal() {
}

(slice) encode_address(slice Address) method_id {
}

```


**typehelpers.fc**
```
forall X -> (tuple, X) ~tpop(tuple t) asm "TPOP";
int tuple_length(tuple t) asm "TLEN";
forall X -> int is_null(X x) asm "ISNULL";
forall X -> int is_int(X x) asm "<{ TRY:<{ 0 PUSHINT ADD DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_cell(X x) asm "<{ TRY:<{ CTOS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_slice(X x) asm "<{ TRY:<{ SBITS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_tuple(X x) asm "ISTUPLE";
forall X -> cell force_cast_to_cell(X x) asm "NOP";
forall X -> slice force_cast_to_slice(X x) asm "NOP";
forall X -> int force_cast_to_int(X x) asm "NOP";
forall X -> tuple force_cast_to_tuple(X x) asm "NOP";
```
