from hypothesis import given, strategies as st

# 1. Base Strategy: digits and constants
# constant = digit {digit}
# Using map(str) ensures we work with strings rather than integers
constant = st.integers(min_value=0, max_value=999).map(str)

@st.composite
def factor(draw):
    """
    factor = constant | "(" expression ")"
    """
    # Randomly decide if we go deeper into a nested expression or stay at a constant
    if draw(st.booleans()):
        # We use deferred() to reference 'expression' before it is fully defined
        nested_expr = draw(st.deferred(expression))
        return f"({nested_expr})"
    return draw(constant)

@st.composite
def term(draw):
    """
    term = factor { ("*" | "/") factor }
    """
    # Start with at least one factor
    result = draw(factor())
    
    # Generate a list of (operator, factor) pairs to simulate the { ... } repetition
    # max_size=2 helps keep the generated strings readable
    extra_factors = draw(st.lists(
        st.tuples(st.sampled_from(["*", "/"]), factor()), 
        max_size=2
    ))
    
    for op, next_f in extra_factors:
        result = f"{result} {op} {next_f}"
    return result

@st.composite
def expression(draw):
    """
    expression = term { ("+" | "-") term }
    """
    result = draw(term())
    
    # Similarly, simulate the repetition of terms
    extra_terms = draw(st.lists(
        st.tuples(st.sampled_from(["+", "-"]), term()), 
        max_size=2
    ))
    
    for op, next_t in extra_terms:
        result = f"{result} {op} {next_t}"
    return result

def expr():
    """Wrapper function to match the requested @given(expr()) syntax."""
    return expression()

@given(expr())
def test_print(expr: str):
    """
    Hypothesis will call this multiple times with different generated strings.
    Run with 'pytest -s' to see the output.
    """
    print(expr)
    assert isinstance(expr, str)
