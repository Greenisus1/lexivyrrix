"""Original offline five-letter deduction game. No official Wordle assets or daily puzzle feed."""
import curses,random,string
from collections import Counter
from pathlib import Path
from ui import put,run
WORDS=tuple(sorted(set(Path(__file__).with_name('words.txt').read_text().split())))
assert WORDS and all(len(w)==5 and w.isascii() and w.isalpha() and w.islower() for w in WORDS)
def score(answer,guess):
 if len(answer)!=5 or len(guess)!=5:raise ValueError('Five letters required')
 marks=[2 if a==g else 0 for a,g in zip(answer,guess)]
 left=Counter(a for a,m in zip(answer,marks) if m!=2)
 for i,g in enumerate(guess):
  if marks[i]!=2 and left[g]>0:marks[i]=1;left[g]-=1
 return marks
class Game:
 def __init__(self,answer=None):
  self.answer=answer or random.choice(WORDS)
  if self.answer not in WORDS:raise ValueError('Answer outside bundled words')
  self.guesses=[];self.marks=[];self.keyboard={}
 @property
 def won(self):return bool(self.guesses and self.guesses[-1]==self.answer)
 @property
 def over(self):return self.won or len(self.guesses)>=6
 def submit(self,guess):
  guess=guess.lower()
  if self.over:return 'Round finished. Esc then N starts another.'
  if len(guess)!=5:return 'Enter five letters.'
  if guess not in WORDS:return 'Not in this game\'s bundled word list.'
  marks=score(self.answer,guess);self.guesses.append(guess);self.marks.append(marks)
  for ch,m in zip(guess,marks):self.keyboard[ch]=max(m,self.keyboard.get(ch,-1))
  return 'Solved!' if self.won else 'Answer: '+self.answer.upper() if self.over else ''
def loop(s):
 g=Game();typed='';msg='';commands=False
 while True:
  h,w=s.getmaxyx();s.erase();put(s,1,2,'L E X I V Y R R I X',curses.A_BOLD)
  if h<25 or w<52:put(s,3,2,'Resize to52x25. Esc then Q exits.')
  else:
   cw=max(6,min(12,(w-10)//5));x=(w-cw*5)//2
   put(s,2,2,'5 letters / 6 guesses / random offline rounds')
   for r in range(6):
    text=g.guesses[r] if r<len(g.guesses) else typed if r==len(g.guesses) else ''
    for c in range(5):
     m=g.marks[r][c] if r<len(g.marks) else -1
     color=curses.color_pair({2:2,1:4,0:5,-1:1}[m]) if curses.has_colors() else 0
     letter=text[c].upper() if c<len(text) else '_'
     put(s,4+r*2,x+c*cw,('[ '+letter+' ]').center(cw-1),color|curses.A_BOLD)
   for row,letters in enumerate(('qwertyuiop','asdfghjkl','zxcvbnm')):
    xx=(w-len(letters)*4)//2
    for col,ch in enumerate(letters):
     m=g.keyboard.get(ch,-1);color=curses.color_pair({2:2,1:4,0:5,-1:1}[m]) if curses.has_colors() else 0
     put(s,17+row,xx+col*4,ch.upper(),color|curses.A_BOLD)
   put(s,h-5,2,msg or 'Green correct / Yellow elsewhere / Gray absent')
   put(s,h-4,2,'Type letters | Enter guess | Backspace erase')
   put(s,h-3,2,'Esc: commands, then N new / Q quit / Esc back' if not commands else 'COMMANDS: N new round / Q quit / Esc back')
   if not curses.has_colors() and g.marks:put(s,h-2,2,'Latest marks: '+' '.join({2:'G',1:'Y',0:'-'}[m] for m in g.marks[-1]))
  s.refresh();k=s.getch()
  if k==27:commands=not commands;continue
  if commands:
   if k in (ord('q'),ord('Q')):return
   if k in (ord('n'),ord('N')):g=Game();typed='';msg='';commands=False
   continue
  if h<25 or w<52:continue
  if k in (10,13,curses.KEY_ENTER):
   msg=g.submit(typed)
   if len(g.guesses)>0 and typed==g.guesses[-1]:typed=''
  elif k in (curses.KEY_BACKSPACE,127,8):typed=typed[:-1]
  elif 0<=k<128 and chr(k).lower() in string.ascii_lowercase and not g.over and len(typed)<5:typed+=chr(k).lower()
if __name__=='__main__':raise SystemExit(run(loop))
