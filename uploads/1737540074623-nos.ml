
    [@@@ocaml.warning "-8"];;


    let rec nos (stmt, state) =
    match stmt with
    | Ass (x, e) -> update x e state
    | Skip -> state
    | Comp (s1, s2) -> let new_state = nos (s1, state) in nos (s2, new_state)
    | If (b, s1, s2) -> if solve_b b state then nos (s1, state) else nos (s2, state)
    | While (b, s) -> 
        let rec loop current_state =
            if solve_b b current_state then
            let new_state = nos (s, current_state) in
            loop new_state
            else current_state
    (* tests *) 

    print_string "x = ";;
    print_int (let new_state = nos (Ast.test1, Semantics.s0) in new_state "x");;
    print_endline "";;

    print_string "x = ";;
    print_int (let new_state = nos (Ast.test2, Semantics.s0) in new_state "x");;
    print_endline "";;

    print_string "x = ";;
    print_int (let new_state = nos (Ast.test3, Semantics.s0) in new_state "x");;
    print_endline "";;

    print_string "x = ";;
    print_int (let new_state = nos (Ast.test4, Semantics.s1) in new_state "x");;
    print_endline "";;

    print_string "y = ";;
    print_int (let new_state = nos (Ast.test4, Semantics.s1) in new_state "y");;
    print_endline "";;

