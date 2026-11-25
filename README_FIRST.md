# Capstone – Madhur Mangla, 2501350087, K = 87

## Files
- assembler.py   Part B (Python assembler, extra feature = symbols.txt)
- Box.asm / Box.hack   Part C
- symbols.txt   output of the extra feature for Box.asm
- hdl/   put your CPU.hdl, Memory.hdl, Computer.hdl here
- report/Capstone_Report_Madhur_Mangla_2501350087.docx   report to finish and upload
- VIVA_CHEATSHEET.md   read before the viva
- WEBSITE_POST.txt   text for the university website

## Do in this order
1. Install Python 3 and the Nand2Tetris Software Suite (nand2tetris.org). Unzip this folder into your lab repo as `capstone/`.
2. Copy your HDL files into hdl/.
3. Part A: Hardware Simulator -> run CPU, Memory, ComputerAdd, ComputerMax, ComputerRect tests. Screenshot each "Comparison ended successfully". Failing chip? Use the built-in one and write it in the report.
4. Part B: open a terminal in this folder:
     python assembler.py Box.asm
   Then take Add.asm, Max.asm, Rect.asm, Pong.asm (from the Nand2Tetris software folder, projects/6). Run each through assembler.py AND the official Assembler. Compare .hack files (or use the official "Load Comparison file"). Screenshot each match.
5. Part C: CPU Emulator -> Load Program -> Box.hack. Click the keyboard box, hold a key, run. Screenshot the black box. Release the key for the optional second screenshot.
6. Report: open the .docx, paste screenshots into the grey boxes, fill the "built-in chips" line, replace the yellow "mistake" paragraph with your real one (keep it 3-4 pages), save as PDF if ZOSIMA needs it, then upload.
7. GitHub (inside your repo folder):
     git add capstone
     git commit -m "Capstone: assembler and Box"
     git push
8. Website: paste WEBSITE_POST.txt, add your GitHub link and 1-2 screenshots.
9. Viva: read VIVA_CHEATSHEET.md; open assembler.py, Box.asm and the CPU Emulator before you go in.
