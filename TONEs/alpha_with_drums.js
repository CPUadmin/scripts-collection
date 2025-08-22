async function startAlphaCat() {
  await Tone.start();
  Tone.Transport.stop();
  Tone.Transport.cancel();
  Tone.Transport.bpm.value = 90;

  // Синтетический kick (ту)
  const kick = new Tone.MembraneSynth({
    pitchDecay: 0.05,
    octaves: 6,
    oscillator: { type: "sine" },
    envelope: { attack: 0.001, decay: 0.3, sustain: 0, release: 0.1 }
  }).toDestination();

  // Синтетический хэт (тсс)
  const hat = new Tone.NoiseSynth({
    noise: { type: "white" },
    envelope: { attack: 0.001, decay: 0.08, sustain: 0 }
  }).toDestination();

  // Ритм: ту ту тсс — ту ту тсс
  const pattern = [
    "kick", "kick", "hat", null,
    "kick", "kick", "hat", null
  ];

  let step = 0;
  Tone.Transport.scheduleRepeat(time => {
    const sound = pattern[step % pattern.length];
    if (sound === "kick") kick.triggerAttackRelease("C1", "8n", time);
    if (sound === "hat")  hat.triggerAttackRelease("16n", time);
    step++;
  }, "8n");

  // Бас (синтетический, жирный)
  const bass = new Tone.MonoSynth({
    oscillator: { type: "square" },
    envelope: { attack: 0.01, decay: 0.2, sustain: 0.3, release: 0.4 }
  }).toDestination();

  const bassline = ["A0", null, "C1", null, "F0", null, null, null];
  let i = 0;
  Tone.Transport.scheduleRepeat(time => {
    const note = bassline[i % bassline.length];
    if (note) bass.triggerAttackRelease(note, "8n", time);
    i++;
  }, "8n");

  Tone.Transport.start();
}
