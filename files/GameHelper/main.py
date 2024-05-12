import sys
sys.dont_write_bytecode = 1

from fetcher import *

def main() -> None:
    if len(sys.argv)>1:
        Fetcher.Notify = True
    else:
        dirs = {} 
    
        if os.path.exists(Fetcher.TargetDir):
            for i in os.listdir(Fetcher.TargetDir):
                d = Fetcher.TargetDir+i+"\\History"
                if (os.path.exists(d)): 
                    dirs[i] = d

        if not os.path.exists(Fetcher.Out): 
            os.mkdir(Fetcher.Out)

        for i in dirs:
            shutil.copy(dirs[i], f"{Fetcher.Out}{i}")
  
    Fetcher.Run()

if __name__=="__main__":
    main()