from pathlib import Path
import threading
from wasmtime import Config, Engine, Linker, Module, Store, WasiConfig


class WasmRuntime:
    def __init__(self, wasm_path: Path, argv: tuple):
        self.wasm_file = wasm_path
        if not self.wasm_file.exists():
            raise FileNotFoundError("WASM file not found")
        
        self.runtime_config = Config()
        self.runtime_config.epoch_interruption = True
        self.runtime_config.consume_fuel = True
        self.runtime_config.cache = True
        
        self.engine = Engine(self.runtime_config)
        self.linker = Linker(self.engine)
        self.linker.define_wasi()
        
        self.module = Module.from_file(self.engine, str(self.wasm_file))
        
        self.wasi = WasiConfig()
        self.wasi.argv = argv
        self.wasi.stdout_file = 'output.log'
        self.wasi.stderr_file = 'error.log'
        
        self.store = Store(self.engine)
        self.store.set_fuel(500_000_000_000)
        self.store.set_epoch_deadline(-1)
        self.store.set_limits(memory_size=1024 * 1024 * 20)
        self.store.set_wasi(self.wasi)
        self.instance = self.linker.instantiate(self.store, self.module)


class PythonWasmRuntime(WasmRuntime):
    def __init__(self, python_code: str = None):
        wasm_path = Path("./python/python-3.12.0.wasm")
        argv = ("python", "-c", python_code if python_code else "")
        super().__init__(wasm_path, argv)


class WasmExecutor:
    def __init__(self, wasm_config: WasmRuntime, timeout: int = 30):
        self.config = wasm_config
        self.timeout = timeout
        self.thread = None
        self.running = False

    def call_function(self, function_name: str, *args):
        return self.config.instance.exports(self.config.store)[function_name](self.config.store, *args)
    
    def start(self, timeout=None):
        if self.running:
            raise RuntimeError("WASM execution already running")
            
        if timeout is None:
            timeout = self.timeout

        result = [None]
        error = [None]
        self.running = True
        
        def run_wasm():
            try:
                result[0] = self.call_function("_start")
            except Exception as e:
                error[0] = e
        
        self.thread = threading.Thread(target=run_wasm)
        self.thread.start()
        self.thread.join(timeout)
        
        if self.thread.is_alive():
            self.stop()
            raise TimeoutError(f"WASM execution timed out after {timeout} seconds")
        
        self.running = False
        if error[0]:
            raise error[0]
        return result[0]

    def stop(self):
        if not self.running:
            return
            
        self.config.store.set_fuel(0)
        if self.thread and self.thread.is_alive():
            self.thread.join()
        self.running = False


if __name__ == "__main__":
    python_code = """
print('Hello from Python WASM!')
x = 5 + 3
print(f'Result: {x}')
"""
    config = PythonWasmRuntime(python_code)
    executor = WasmExecutor(config, timeout=10)
    
    try:
        result = executor.start()
        
        with open('output.log', 'r') as f:
            print("Output:", f.read())
        
        with open('error.log', 'r') as f:
            error = f.read()
            if error:
                print("Errors:", error)
                
    except TimeoutError as e:
        print(f"Execution timed out: {e}")
    except Exception as e:
        print(f"Error during execution: {e}")
