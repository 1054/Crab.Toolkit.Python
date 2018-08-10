/*
  About using C++ in Python code, see -- https://docs.python.org/3/extending/building.html#building
  Compile this code as: `clang -I/opt/local/Library/Frameworks/Python.framework/Versions/3.6/include/python3.6m -c lib_test_1.cpp -o lib_test_1.so`
*/

#include <Python.h>
#include <cstdlib>
#include <iostream>

using namespace std;


__attribute__((unused))
static PyObject* hello(PyObject *self, PyObject *args) {
    printf("Hello\n");
    Py_RETURN_NONE;
}



__attribute__((unused))
static PyObject* test(PyObject *self, PyObject *args)
{
    const char* command;

    int sts;

    if (!PyArg_ParseTuple(args, "s", &command)) {
        // if no input args then return NULL
        return NULL;
    }

    std::cout << command << std::endl;

    sts = system(command);

    return Py_BuildValue("i", sts); // return the value of sts as Python object. This is done using the function Py_BuildValue().
    // If you have a C function that returns no useful argument (a function returning void), the corresponding Python function must return None. You need this idiom to do so (which is implemented by the Py_RETURN_NONE macro):
    //   Py_INCREF(Py_None);
    //   return Py_None;

}



// Method definition object for this extension, these argumens mean:
// ml_name: The name of the method
// ml_meth: Function pointer to the method implementation
// ml_flags: Flags indicating special features of this method, such as
//          accepting arguments, accepting keyword arguments, being a
//          class method, or being a static method of a class.
// ml_doc:  Contents of this method's docstring
static PyMethodDef lib_test_1_methods[] = {
    {
        "hello",
        hello,
        METH_NOARGS,
        "Print 'hello world' from a method defined in a C extension."
    },
    {
        "test",
        test,
        METH_VARARGS,
        "test"
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};






// Module definition
// The arguments of this structure tell Python what to call your extension,
// what it's methods are and where to look for it's method definitions
static struct PyModuleDef lib_test_1_definition = {
    PyModuleDef_HEAD_INIT,
    "lib_test_1",
    "",
    -1,
    lib_test_1_methods
};



// Module initialization
// Python calls this function when importing your extension. It is important
// that this function is named PyInit_[[your_module_name]] exactly, and matches
// the name keyword argument in setup.py's setup() call.
PyMODINIT_FUNC
PyInit_lib_test_1(void)
{
    Py_Initialize();
    PyObject *m;
    m = PyModule_Create(&lib_test_1_definition);
    return m;
}






