# PyRLE
RLE encoding for binary files using Python
<br>
Instructions are in the .py file header. Supports 2 RLE encoding methods.<br>
<br>
## Z80 Decryption Routine (tniasm)<br>
```
DecompressRLE:
;;;;;;;;;;;;;;
    ;;;;
    ; HL - mem addr of compressed data 
    ; DE - system ram destination of decompressed data
    ; BC - size of compressed data
    ;ld a, $7f          ; these four lines check if the data to load is < $8000,
    ;cp h               ;  and if so, swaps page 1 to the cartridge ROM.
    ;jr c, .loop_a
    ; call Page1CartROM
.loop_a:
    push bc 
    ld a, (hl) 
    inc hl 
    ld b, a         ; b has original byte
    ld a, (hl)      
    cp b
    jr z, .dupe     ; are b0 and b1 the same?
     ; if not
     ld a, b
     ld (de), a 
     inc de         ; write b0 to de++
     pop bc 
     dec bc 
     ld a, $ff      ; did b loop back around?
     cp b
     jr nz, .loop_a
     ret 
.dupe:
    ; if they are, lets just skip
    inc hl          ; b2 is the reps
    ld a, (hl)
    inc hl          ; b3 is wher we want to be
    ld c, a         ; c has reps
    ld a, b         ; byte to write back to a
.dupeloop:
    ld (de), a 
    inc de 
    dec c 
    jr nz, .dupeloop
    pop bc 
    dec bc
    dec bc 
    dec bc
    ld a, $ff 
    cp b 
    jr nz, .loop_a
     ; call Page1MainROM    ; if necessary
     ret
     ```
