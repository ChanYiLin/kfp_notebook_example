import kfp
import kfp.gcp
import kfp.dsl as dsl
import kfp.compiler
import kfp.components
from kfp.components import func_to_container_op, InputPath, OutputPath
client = kfp.Client(host="https://kubeflow-appinst-densa.appier.us/")


add_op = kfp.components.load_component(filename='./add.yaml')
divmod_op = kfp.components.load_component(filename='./divmod.yaml')


@dsl.pipeline(
    name='Calculation pipeline',
    description='A toy pipeline that performs arithmetic calculations.'
)
def add_div_pipeline(
    a='1',
    b='7',
    c='17',
):
    #Passing pipeline parameter and a constant value as operation arguments
    add_task = add_op(a, 4) #Returns a dsl.ContainerOp class instance. 
    add_task.set_image_pull_policy('Always')
    
    #Passing a task output reference as operation arguments
    #For an operation with a single return value, the output reference can be accessed using `task.output` or `task.outputs['output_name']` syntax
    divmod_task = divmod_op(add_task.output, b)
    divmod_task.set_image_pull_policy('Always')

    #For an operation with a multiple return values, the output references can be accessed using `task.outputs['output_name']` syntax
    result_task = add_op(divmod_task.outputs['quotient'], c)
    result_task.set_image_pull_policy('Always')


# Specify pipeline argument values
arguments = {'a': '7', 'b': '8'}
# Submit a pipeline run
client.create_run_from_pipeline_func(add_div_pipeline, arguments=arguments, experiment_name="test", run_name="reuse_components")