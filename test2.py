from Interpreter import Interpreter

text = """
to construct midpoint point M given point A, point B do
    define circle[A, B] ∩ circle[B, A] as C, D
    define line[C, D] ∩ line[A, B] as M
done

to construct perpendicolare ray r given point A, point B do
    with
    circle[A, B] ∩1 ray[B, A] as C and
    circle[B, C] ∩0 circle[C, B] as T do
        define ray[A, T] as r
    done
done


to construct pentagono point C, point D, point E given point A, point B do
    define midpoint(A, B) as M
    define circle[B, A] ∩ perpendicolare(B, A) as T
    define circle[M, T] ∩ ray[A, B] as P
    define circle[A, P] ∩ perpendicolare(M, A) as D
    define circle[A, P] ∩0 circle[B, A] as C
    with circle[M, P] ∩ ray[B, A] as R do
        define circle[B, R] ∩1 circle[A, B] as E 
    done
done

to construct main given point A, point B do
    define pentagono(A, B) as C, D, E
    
    with
    circle[A, B] ∩0 circle[B, A] as M and
    ray[A, B] ∩ ray[D, C] as R do
        define circle[M, R] as cerchio
    done

    with
    line[A, B] ∩ cerchio as DE, AB and
    line[B, C] ∩ cerchio as EA, BC and
    line[C, D] ∩1 cerchio as CD
    do
        define segment[DE, AB] as a
        define segment[EA, BC] as b
        define segment[AB, CD] as c
        define segment[BC, DE] as d
        define segment[CD, EA] as e
    done
    show
done
"""

interpreter = Interpreter()

if not interpreter.source(text):
    exit()

interpreter((0, 0), (100, 0))