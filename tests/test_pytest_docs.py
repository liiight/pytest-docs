import textwrap


def test_markdown_formatter(testdir, tmp_path):
    path = tmp_path / 'doc.md'
    testdir.makepyfile(
        """
        '''This is the module doc'''
        import pytest
        
        pytestmark = [pytest.mark.module_mark, pytest.mark.module_mark_2, pytest.mark.pytest_doc(name='Test Docs')]
        
        
        @pytest.mark.class_marker
        @pytest.mark.pytest_doc(name='Test Class')
        class TestClass:
            '''This is the class doc'''
        
            @pytest.mark.func_mark_a('foo')
            def test_func_a(self):
                '''This is the doc for test_func_a'''
                assert 1
        
            @pytest.mark.kwarg_mark(goo='bla')
            def test_func_b(self):
                '''This is the doc for test_func_b'''
                assert 1
        
        """)
    testdir.runpytest(
        '--docs', '{}'.format(path)
    )
    assert path.read_text() == textwrap.dedent("""\
    # Test Docs
    This is the module doc
    
    **Markers:**
    - module_mark  
    - module_mark_2  
    - pytest_doc  (name=Test Docs)
    ## Test Class
    This is the class doc
    
    **Markers:**
    - pytest_doc  (name=Test Class)
    - class_marker  
    ### test_func_a
    This is the doc for test_func_a
    
    **Markers:**
    - func_mark_a (foo) 
    ### test_func_b
    This is the doc for test_func_b
    
    **Markers:**
    - kwarg_mark  (goo=bla)
    """)
