from ipykernel.kernelapp import IPKernelApp
from .kernel import ElasticsearchKernel


IPKernelApp.launch_instance(kernel_class=ElasticsearchKernel)
