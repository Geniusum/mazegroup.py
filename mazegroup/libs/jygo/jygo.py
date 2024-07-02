import jygo.lib.consts as consts
import jygo.lib.base.errors as errors
import jygo.lib.base.jumps as jumps
import jygo.lib.base.logs as logs

class Script():
    def __init__(self) -> None:
        self.main = consts.void()
    
    def setMain(self, func:any):
        self.main = func

    def run(self):
        try:
            jumps.Jump()
            logs.Log("Starting main function...").show()
            jumps.Jump()
            e = self.main()
            jumps.Jump()
            logs.Log("Main function finished").show()
            if e:
                errors.Error("Main function exception : " + str(e)).show()
        except Exception as e:
            errors.Error(f"Error in main function : {e}").show()